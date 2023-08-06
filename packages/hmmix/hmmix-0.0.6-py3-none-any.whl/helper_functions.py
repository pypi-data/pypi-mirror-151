import numpy as np
import json
from collections import defaultdict
import os
import itertools
import difflib
from glob import glob

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Make test data
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def Maketestdata(data_set_length):
    '''Create test data set of size data_set_length. Also create uniform weights and uniform mutation rates'''
    np.random.seed(42)


    window_size = 1000
    mutation_rate_window = 1000000

    # Initialization parameters (prob of staring in states)
    state_values = [0,1]
    state_names, transitions, emissions, starting_probabilities = get_default_HMM_parameters()

    print('creating 2 chromosomes with 50 Mb of test data (100K bins) with the following parameters..\n')
    print('State names:', state_names)
    print('Starting_probabilities:', starting_probabilities)
    print('Transition matrix:')
    print(transitions)
    print('Emission values:',emissions)   


    mutation_matrix = {
        'A': [0, 0.16, 0.68, 0.16],
        'C': [0.16, 0,0.16, 0.68],
        'G': [0.68, 0.16, 0, 0.16],
        'T': [0.16, 0.68, 0.16, 0],
    }

    bases = ['A','C','G','T']

    # Make obs file
    with open('obs.txt','w') as obs:

        print('chrom', 'pos', 'ancestral_base', 'genotype', sep = '\t', file = obs)

        for chrom in ['chr1', 'chr2']:
            for index in range(data_set_length):
                if index == 0:
                    current_state = np.random.choice(state_values, p=starting_probabilities)
                else:
                    current_state = np.random.choice(state_values, p=transitions[prevstate] )

                n_mutations = np.random.poisson(lam=emissions[current_state]) 
                for mutation in [int(x) for x in np.random.uniform(low=index*window_size, high=index*window_size + window_size, size=n_mutations)]: 
                    ancestral_base = np.random.choice(bases, p=[0.31, 0.19, 0.19, 0.31])
                    derived_base = np.random.choice(bases, p=mutation_matrix[ancestral_base])
                    print(chrom, mutation, ancestral_base, ancestral_base + derived_base, sep = '\t', file = obs)          

                prevstate = current_state


    # Make mutation file
    with open('mutrates.bed','w') as mutrates:
        for chrom in ['chr1', 'chr2']:
            for start in range(int(data_set_length * window_size / mutation_rate_window)):
                print(chrom, start * mutation_rate_window, (start + 1) * mutation_rate_window, 1, sep = '\t', file = mutrates)



    # Make weights file
    with open('weights.bed','w') as weights:
        for chrom in ['chr1', 'chr2']:
            print(chrom, 1, data_set_length * window_size, sep = '\t', file = weights)



    # Make initial guesses
    state_names = np.array(['Human', 'Archaic'])
    starting_probabilities = np.array([0.5, 0.5])
    transitions = np.array([[0.99,0.01],[0.02,0.98]])
    emissions = np.array([0.03, 0.3])

    Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions, 'Initialguesses.json')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions for handling HMM parameters
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def get_default_HMM_parameters():
    '''Creates human/neanderthal introgression like HMM parameters'''
    state_names = np.array(['Human', 'Archaic'])
    starting_probabilities = np.array([0.98, 0.02])
    transitions = np.array([[0.9999,0.0001],[0.02,0.98]])
    emissions = np.array([0.04, 0.4])

    return state_names, transitions, emissions, starting_probabilities



def Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions, outfile):
    '''Saves parameters to a file'''
    json_string = json.dumps({
                'state_names' : state_names.tolist(),
                'starting_probabilities' : starting_probabilities.tolist(),
                'transitions' : transitions.tolist(),
                'emissions' : emissions.tolist(),
             }, indent = 2)

    Make_folder_if_not_exists(outfile)
    with open(outfile, 'w') as out:
        out.write(json_string)


def Load_HMM_parameters(markov_param):
    '''Loads parameters to a file'''
    if markov_param is None:
        state_names, transitions, emissions, starting_probabilities = get_default_HMM_parameters()
    else:
        with open(markov_param) as json_file:
            data = json.load(json_file)

        state_names, starting_probabilities, transitions, emissions = data['state_names'], data['starting_probabilities'], data['transitions'], data['emissions']


    # convert into numpy arrays
    transitions, starting_probabilities, emissions, state_names = np.array(transitions), np.array(starting_probabilities), np.array(emissions), np.array(state_names)

    return state_names, transitions, emissions, starting_probabilities


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions for handling observertions/bed files
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def convert_to_bases(genotype, ref, alt):

    both_bases = ref + alt

    if '|' in genotype:
        base1, base2 = [int(x) for x in genotype.split('|')]
        return both_bases[base1] + both_bases[base2]
    elif '/':
        base1, base2 = [int(x) for x in genotype.split('/')]
        return both_bases[base1] + both_bases[base2]
    



def make_callability_from_bed(bedfile, window_size):
    callability = defaultdict(lambda: defaultdict(float))
    with open(bedfile) as data:
        for line in data:

            if not line.startswith('chrom'):

                if len(line.strip().split('\t')) == 3:
                    chrom, start, end = line.strip().split('\t')
                    value = 1
                elif  len(line.strip().split('\t')) > 3:
                    chrom, start, end, value = line.strip().split('\t')[0:4]
                    value = float(value)

                start = int(start)
                end = int(end)


                firstwindow = start - start % window_size
                firstwindow_fill = window_size - start % window_size

                lastwindow = end - end % window_size
                lastwindow_fill = end %window_size

                # not spanning windows
                if firstwindow == lastwindow:
                    callability[chrom][firstwindow] += (end-start+1) * value

                else:

                    callability[chrom][firstwindow] += firstwindow_fill * value
                    callability[chrom][lastwindow] += (lastwindow_fill+1) * value

                    for window_tofil in range(firstwindow + window_size, lastwindow, window_size):
                        callability[chrom][window_tofil] += window_size * value

    return callability



def Load_observations_weights_mutrates(obs_file, mutrates_file, weights_file, window_size, haploid):

    obs_counter = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    if haploid:
        haplotypes = defaultdict(int)
        with open(obs_file) as data:
            for line in data:
                if not line.startswith('chrom'):
                    chrom, pos, ancestral_base, genotype = line.strip().split()
                    rounded_pos = int(pos) - int(pos) % window_size
                    for i, base in enumerate(genotype):
                        if base != ancestral_base:
                            obs_counter[chrom][rounded_pos][f'haploid_{i+1}'] += 1
                            haplotypes[f'haploid_{i+1}'] += 1
    else:
        haplotypes = defaultdict(int)
        with open(obs_file) as data:
            for line in data:
                if not line.startswith('chrom'):
                    chrom, pos, ancestral_base, genotype = line.strip().split()
                    rounded_pos = int(pos) - int(pos) % window_size
                    obs_counter[chrom][rounded_pos]['diploid'] += 1
                    haplotypes['diploid'] += 1

    temp_obs = []
    for haplotype in sorted(haplotypes):
        for chrom in sorted(obs_counter, key=sortby):
            lastwindow = max(obs_counter[chrom]) + window_size

            for window in range(0, lastwindow, window_size):
                temp_obs.append(obs_counter[chrom][window][haplotype])

    # Read weights file is it exists - else set all weights to 1
    if weights_file is None:
        weights = np.ones(len(temp_obs)) 
    else:  
        callability = make_callability_from_bed(weights_file, window_size)
        weights = []
        for haplotype in sorted(haplotypes):
            for chrom in sorted(obs_counter, key=sortby):
                lastwindow = max(obs_counter[chrom]) + window_size

                for window in range(0, lastwindow, window_size):
                    weights.append(callability[chrom][window] / float(window_size))


    # Read mutation rate file is it exists - else set all mutation rates to 1
    if mutrates_file is None:
        mutrates = np.ones(len(temp_obs)) 
    else:  
        callability = make_callability_from_bed(mutrates_file, window_size)
        mutrates = []
        for haplotype in sorted(haplotypes):
            for chrom in sorted(obs_counter, key=sortby):
                lastwindow = max(obs_counter[chrom]) + window_size

                for window in range(0, lastwindow, window_size):
                    mutrates.append(callability[chrom][window] / float(window_size))

    # Make sure there are no places with obs > 0 and 0 in mutation rate or weight
    obs = np.zeros(len(temp_obs))
    for index, (observation, w, m) in enumerate(zip(temp_obs, weights, mutrates)):
        if w*m == 0 and observation != 0:
            obs[index] = 0
            print('warning, you had observations but no called bases/no mutation rate')
            print(index, observation, w, m)
        else:
            obs[index] = int(observation)

    return obs.astype(int), np.array(mutrates).astype(float), np.array(weights).astype(float)



def Get_genome_coordinates(obs_file, window_size, haploid):
    

    obs_counter = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    if haploid:
        haplotypes = defaultdict(int)
        with open(obs_file) as data:
            for line in data:
                if not line.startswith('chrom'):
                    chrom, pos, ancestral_base, genotype = line.strip().split()
                    rounded_pos = int(pos) - int(pos) % window_size
                    for i, base in enumerate(genotype):
                        if base != ancestral_base:
                            obs_counter[chrom][rounded_pos][f'_hap{i+1}'].append(pos)
                            haplotypes[f'_hap{i+1}'] += 1
    else:
        haplotypes = defaultdict(int)
        with open(obs_file) as data:
            for line in data:
                if not line.startswith('chrom'):
                    chrom, pos, ancestral_base, genotype = line.strip().split()
                    rounded_pos = int(pos) - int(pos) % window_size
                    obs_counter[chrom][rounded_pos][''].append(pos)
                    haplotypes[''] += 1

    chroms, starts, variants = [], [], []
    for haplotype in sorted(haplotypes):
        for chrom in sorted(obs_counter, key=sortby):
            lastwindow = max(obs_counter[chrom]) + window_size

            for window in range(0, lastwindow, window_size):
                chroms.append(f'{chrom}{haplotype}')   
                starts.append(window)
                variants.append(','.join(obs_counter[chrom][window][haplotype]))

    return chroms, starts, variants


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# For decoding/training
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def find_runs(inarray):
        """ run length encoding. Partial credit to R rle function. 
            Multi datatype arrays catered for including non Numpy
            returns: tuple (runlengths, startpositions, values) """
        ia = np.asarray(inarray)                # force numpy
        n = len(ia)
        if n == 0: 
            return (None, None, None)
        else:
            y = ia[1:] != ia[:-1]               # pairwise unequal (string safe)
            i = np.append(np.where(y), n - 1)   # must include last element posi
            z = np.diff(np.append(-1, i))       # run lengths
            p = np.cumsum(np.append(0, z))[:-1] # positions
            #return (ia[i], p, z)

            for (a, b, c) in zip(ia[i], p, z):
                yield (a, b, c)


def logoutput(emissions, loglikelihood, transitions, starting_probabilities, iteration):

    if iteration == 0:    
        print_emissions = '\t'.join(['emis{0}'.format(x + 1) for x in range(len(emissions))])
        print_starting_probabilities = '\t'.join(['start{0}'.format(x + 1) for x in range(len(emissions))])
        print_transitions = '\t'.join(['trans{0}_{0}'.format(x + 1) for x in range(len(emissions))])
        print('iteration', 'loglikelihood', print_starting_probabilities, print_emissions, print_transitions, sep = '\t')

    
    print_emissions = '\t'.join([str(x) for x in np.matrix.round(emissions, 4)])
    print_starting_probabilities = '\t'.join([str(x) for x in np.matrix.round(starting_probabilities, 3)])
    print_transitions = '\t'.join([str(x) for x in np.matrix.round(transitions, 4).diagonal()])
    print(iteration, round(loglikelihood, 4), print_starting_probabilities, print_emissions, print_transitions, sep = '\t')


def get_ancestral_from_fasta(ancestral):
    '''
    Read a fasta file with a single chromosome in and return the sequence as a string

    Ancestra.fa

    >seq1
    AGCATCGATCGACTGACTA

    get_ancestral_from_fasta(Ancestra.fa) returns AGCATCGATCGACTGACTA   
    '''

    ancestral_allele = ''
    with open(ancestral) as data:
        for line in data:
            if line.startswith('>'):
                pass
                #seqname = line.strip().replace('>','')
            else:
                ancestral_allele += line.strip().upper()

    return ancestral_allele


def make_mutation_rate(freqfile, outfile, callablefile, window_size):

    print('-' * 40)
    print('Selected parameters')
    print(f'> Outgroupfile is:\n{freqfile}\n')
    print(f'> Outputfile is:\n{outfile}\n')
    print(f'> Callability file is:\n{callablefile}\n')
    print(f'> Window size is:\n{window_size}\n')
    print('-' * 40)

    snps_counts_window = defaultdict(lambda: defaultdict(int))

    with open(freqfile) as data:
        for line in data:
            if not line.startswith('chrom'):
                chrom, pos = line.strip().split()[0:2]
                # _, ref_count = ref_allele_info.split(':')
                # _, alt_count = alt_allele_info.split(':')
                # pos, ref_count, alt_count = int(pos),  int(ref_count), int(alt_count)
                pos = int(pos)
                window = pos - pos%window_size
                snps_counts_window[chrom][window] += 1


    mutations = []
    genome_positions = []
    for chrom in sorted(snps_counts_window, key=sortby):
        lastwindow = max(snps_counts_window[chrom]) + window_size

        for window in range(0, lastwindow, window_size):
            mutations.append(snps_counts_window[chrom][window])
            genome_positions.append([chrom, window, window + window_size])

    mutations = np.array(mutations)

    if callablefile is not None:
        callability = make_callability_from_bed(callablefile, window_size)
        callable_region = []
        for chrom in sorted(snps_counts_window, key=sortby):
            lastwindow = max(snps_counts_window[chrom]) + window_size
            for window in range(0, lastwindow, window_size):
                callable_region.append(callability[chrom][window]/window_size)
    else:
        callable_region = np.ones(len(mutations)) * window_size

    genome_mean = np.sum(mutations) / np.sum(callable_region)

    Make_folder_if_not_exists(outfile)
    with open(outfile,'w') as out:
        print('chrom', 'start', 'end', 'mutationrate', sep = '\t', file = out)
        for genome_pos, mut, call in zip(genome_positions, mutations, callable_region):
            chrom, start, end = genome_pos
            if mut * call == 0:
                ratio = 0
            else:
                ratio = round(mut/call/genome_mean, 2)

            print(chrom, start, end, ratio, sep = '\t', file = out)
        

def get_consensus(infiles):
    '''
    Find consensus prefix, postfix and value that changes in set of files:

    myfiles = ['chr1.vcf', 'chr2.vcf', 'chr3.vcf']
    prefix, postfix, values = get_consensus(myfiles) 
    
    prefix=chr
    postfix=.vcf
    values = {1,2,3} -> is a set
    '''
    infiles = [str(x) for x in infiles]

    consensus_strings = defaultdict(int)
    for a, b in itertools.combinations(infiles,2):
        consensus_a = 'START'
        for i,s in enumerate(difflib.ndiff(a, b)):
            if s[0] != ' ':
                consensus_a += ' '
            else:
                consensus_a += s[-1]
        consensus_a += 'END'


        new_joined = '|'.join(consensus_a.split()).replace('START','').replace('END','')
        consensus_strings[new_joined] += 1

    for value in consensus_strings:

        if len(value.split('|')) == 2:
            prefix, postfix = value.split('|')
            matches = len([x for x in infiles if prefix in x and postfix in x])

            if matches == len(infiles):
                values = [x.replace(prefix, '').replace(postfix,'') for x in infiles]
                return prefix, postfix, set(values)

def sortby(x):
    '''
    This function is used in the sorted() function. It will sort first by numeric values, then strings then other symbols

    Usage:
    mylist = ['1', '12', '2', 3, 'MT', 'Y']
    sortedlist = sorted(mylist, key=sortby)
    returns ['1', '2', 3, '12', 'MT', 'Y']
    '''

    lower_case_letters = 'abcdefghijklmnopqrstuvwxyz'
    if x.isnumeric():
        return int(x)
    elif type(x) == str and len(x) > 0:
        if x[0].lower() in lower_case_letters:
            return 1e6 + lower_case_letters.index(x[0].lower())
        else:
            return 2e6
    else:
        return 3e6


def Make_folder_if_not_exists(path):
    '''
    Check if path exists - otherwise make it;
    If path is /path/to/my/file.txt this will check if /path/to/my/ exists.
    '''
    path = os.path.dirname(path)
    if path != '':
        if not os.path.exists(path):
            os.makedirs(path)



def Annotate_with_ref_genome(vcffiles, obsfile):
    obs = defaultdict(list)
    shared_with = defaultdict(str)

    tempobsfile = obsfile + 'temp'

    with open(obsfile) as data, open(tempobsfile,'w') as out:
        for line in data:
            if not line.startswith('chrom'):
                out.write(line)
                chrom, pos, ancestral_base, genotype = line.strip().split()
                derived_variant = genotype.replace(ancestral_base, '')[0]
                ID = f'{chrom}_{pos}'
                obs[ID] = [ancestral_base, derived_variant]

    print('Loading in admixpop snp information')
    for vcffile in handle_infiles(vcffiles):
        command = f'bcftools view -a -R {tempobsfile} {vcffile}'
        print(command)

        for line in os.popen(command):
            if line.startswith('#CHROM'):
                individuals_in_vcffile = line.strip().split()[9:]

            if not line.startswith('#'):

                chrom, pos, _, ref_allele, alt_allele = line.strip().split()[0:5]
                ID =  f'{chrom}_{pos}'
                genotypes = [x.split(':')[0] for x in line.strip().split()[9:]]

                ancestral_base, derived_base = obs[ID]
                found_in = []

                for original_genotype, individual in zip(genotypes, individuals_in_vcffile):

                    if '.' not in original_genotype:
                        genotype = convert_to_bases(original_genotype, ref_allele, alt_allele)   

                        if genotype.count(derived_base) > 0:
                            found_in.append(individual)

                if len(found_in) > 0:
                    shared_with[ID] = '|'.join(found_in)


    # Clean log files generated by vcf and bcf tools
    clean_files('out.log')
    clean_files(tempobsfile)

    return shared_with, individuals_in_vcffile

def get_ingroup_or_outgroup(outgroup_ingroupfile, key):
    '''
    reads a json file which has the keys outgroup and ingroup. In both the values should be a string. 
    '''
    with open(outgroup_ingroupfile) as json_file:
        data = json.load(json_file)

    return data[key]

def handle_individuals_input(argument, group_to_choose):
    # Is this a json file?
    if os.path.exists(argument):
        return get_ingroup_or_outgroup(argument, group_to_choose)
    else:
        return argument.split(',')


# Check which type of input we are dealing with
def handle_infiles(input):
    file_list = glob(input)
    if len(file_list) > 0:
        return file_list
    else:
        if ',' in input:
            return input.split(',')
        else:
            return [input]

# Clean up
def clean_files(filename):
    if os.path.exists(filename):
        os.remove(filename)


# Find variants from admixed population
def find_admixed_variants(variants_list):

    flattened_list = []
    for bin in variants_list:
        if bin != '':
            if ',' in bin:
                for position in bin.split(','):
                    flattened_list.append(position)

            else:
                flattened_list.append(bin)

    return flattened_list


