import os
import numpy as np
from collections import defaultdict
import sys 
from glob import glob

from helper_functions import get_ingroup_outgroup, get_ancestral_from_fasta, get_consensus, sortby, Make_folder_if_not_exists, convert_to_bases


# Clean up
def clean_files(filename):
    if os.path.exists(filename):
        os.remove(filename)



# Check which type of input we are dealing with
def makelist(input):
    file_list = glob(input)
    if len(file_list) > 0:
        return file_list
    else:
        if ',' in input:
            return input.split(',')
        else:
            return [input]

# Check which type of input we are dealing with
def combined_files(ancestralfiles, vcffiles):

    if len(ancestralfiles) == len(vcffiles):
        return ancestralfiles, vcffiles


    elif ancestralfiles == ['']:
        if len(vcffiles) > 1:
            prefix1, postfix1, values1 = get_consensus(vcffiles)
            vcffiles = []
            for joined in sorted(values1, key=sortby):
                vcffiles.append(''.join([prefix1, joined, postfix1]))

        ancestralfiles = [None for _ in vcffiles]
        return ancestralfiles, vcffiles
       
    elif len(ancestralfiles) > 1 and len(vcffiles) > 1:
        prefix1, postfix1, values1 = get_consensus(vcffiles)
        prefix2, postfix2, values2 = get_consensus(ancestralfiles)

        vcffiles = []
        ancestralfiles = []

        for joined in sorted(values1.intersection(values2), key=sortby):
            vcffiles.append(''.join([prefix1, joined, postfix1]))
            ancestralfiles.append(''.join([prefix2, joined, postfix2]))
        return ancestralfiles, vcffiles
    
    elif len(ancestralfiles) > 1 and len(vcffiles) == 1:
        prefix2, postfix2, values2 = get_consensus(ancestralfiles)
        ancestralfiles = []
        
        for key in values2:
            if key in vcffiles[0]:
                ancestralfiles.append(''.join([prefix2, key, postfix2]))

        return ancestralfiles, vcffiles

    elif len(ancestralfiles) == 1 and len(vcffiles) > 1:
        prefix1, postfix1, values1 = get_consensus(vcffiles)
        vcffiles = []
        
        for key in values1:
            if key in ancestralfiles[0]:
                vcffiles.append(''.join([prefix1, key, postfix1]))

        if len(vcffiles) > len(ancestralfiles):
            sys.exit('Could not resolve ancestral files and vcffiles (try comma separated values)')


        return ancestralfiles, vcffiles


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Dealing with bcf/vcf files functions
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def make_out_group(outgroup_ingroupfile, bedfile, vcffiles, outputfile, ancestralfiles):

    # Is this a json file?
    if os.path.exists(outgroup_ingroupfile):
        _, outgroup_individuals = get_ingroup_outgroup(outgroup_ingroupfile)
    elif ',' in outgroup_ingroupfile:
        outgroup_individuals = outgroup_ingroupfile.split(',')
    else:
        outgroup_individuals = [outgroup_ingroupfile]

    print('-' * 40)
    print('Selected parameters')
    print('\n> Outgroup individuals:', len(outgroup_individuals))
    print('First 10..')
    for i, x in enumerate(outgroup_individuals):
        print(x)
        if i > 10:
            break
    print()

    vcffiles = makelist(vcffiles)
    ancestralfiles = makelist(ancestralfiles)
    ancestralfiles, vcffiles  = combined_files(ancestralfiles, vcffiles)

    print('> Using vcf and ancestral files')
    for vcffile, ancestralfile in zip(vcffiles, ancestralfiles):
        print('vcffile:',vcffile, 'ancestralfile:',ancestralfile)
    print()    

    print('> Callability file:\n', bedfile, '\n')

    outgroup_individuals = ','.join(outgroup_individuals)
    print(f'> Writing output to:\n',outputfile,'\n')
    print('-' * 40)

    Make_folder_if_not_exists(outputfile)

    with open(outputfile, 'w') as out:

        print('chrom', 'pos', 'ref_allele_info', 'alt_allele_info', 'ancestral_base', sep = '\t', file = out)

        for vcffile, ancestralfile in zip(vcffiles, ancestralfiles):

            if ancestralfile is not None:
                ancestral_allele = get_ancestral_from_fasta(ancestralfile)

            if bedfile is not None:
                command = f'bcftools view -m2 -M2 -v snps -s {outgroup_individuals} -T {bedfile} {vcffile} | vcftools --vcf - --counts --stdout'
            else:
                command = f'bcftools view -m2 -M2 -v snps -s {outgroup_individuals} {vcffile} | vcftools --vcf - --counts --stdout'
            
            print(f'Processing {vcffile}...')
            print('Running command:')
            print(command, '\n\n')

            for index, line in enumerate(os.popen(command)):

                if not line.startswith('CHROM'):

                    chrom, pos, _, _, ref_allele_info, alt_allele_info = line.strip().split()

                    ref_allele, ref_count = ref_allele_info.split(':')
                    alt_allele, alt_count = alt_allele_info.split(':')

                    pos, ref_count, alt_count = int(pos),  int(ref_count), int(alt_count)

                    # Always include polymorphic sites
                    if alt_count > 0 and ref_count > 0:
                        ancestral_base = ref_allele if ref_count > alt_count else alt_allele
                        print(chrom, pos, ref_allele_info, alt_allele_info, ancestral_base, sep = '\t', file = out)

                    # Fixed sites
                    elif alt_count * ref_count == 0:

                        if ref_count == 0:
                            ancestral_base = alt_allele
                            print(chrom, pos, ref_allele_info, alt_allele_info, ancestral_base, sep = '\t', file = out)

                        elif ancestralfile is not None:
                        
                            ancestral_base = ancestral_allele[pos-1]
                            if (ancestral_base == ref_allele.upper() and alt_count > 0) or (ancestral_base == alt_allele.upper() and ref_count > 0):
                                print(chrom, pos, ref_allele_info, alt_allele_info, ancestral_base, sep = '\t', file = out)


                    if index % 100000 == 0:
                        print(f'at line {index} at chrom {chrom} and position {pos}')

    # Clean log files generated by vcf and bcf tools
    clean_files('out.log')
    



def make_ingroup_obs(outgroup_ingroupfile, bedfile, vcffiles, outprefix, outgroupfile, ancestralfiles):

    # Is this a json file?
    if os.path.exists(outgroup_ingroupfile):
        ingroup_individuals, _ = get_ingroup_outgroup(outgroup_ingroupfile)
    elif ',' in outgroup_ingroupfile:
        ingroup_individuals = outgroup_ingroupfile.split(',')
    else:
        ingroup_individuals = [outgroup_ingroupfile]

    print('-' * 40)
    print('Selected parameters')
    print('\n > Ingroup individuals:', len(ingroup_individuals))
    print('First 10')
    for i, x in enumerate(ingroup_individuals):
        print(x)
        if i > 10:
            break
    print()

    vcffiles = makelist(vcffiles)
    ancestralfiles = makelist(ancestralfiles)
    ancestralfiles, vcffiles  = combined_files(ancestralfiles, vcffiles)

    print('> Using vcf and ancestral files')
    for vcffile, ancestralfile in zip(vcffiles, ancestralfiles):
        print('vcffile:',vcffile, 'ancestralfile:',ancestralfile)
    print()  

    print('> Using outgroup variants from:\n', outgroupfile, '\n')  

    print('> Callability file:\n', bedfile, '\n')

    print(f'Writing output to file with prefix:\n{outprefix}.<individual>.txt\n')
    print('-' * 40)

    
    list_of_obs = defaultdict(list)
    ingroup_individuals = ','.join(ingroup_individuals)

    for vcffile, ancestralfile in zip(vcffiles, ancestralfiles):

        if ancestralfile is not None:
            ancestral_allele = get_ancestral_from_fasta(ancestralfile)

        if bedfile is not None:
            command = f'bcftools view -m2 -M2 -v snps -s {ingroup_individuals} -T {bedfile} {vcffile} | vcftools --vcf - --exclude-positions {outgroupfile} --recode --stdout'
        else:
            command = f'bcftools view -m2 -M2 -v snps -s {ingroup_individuals} {vcffile} | vcftools --vcf - --exclude-positions {outgroupfile} --recode --stdout'

        print('Running command:')
        print(command, '\n\n')

        for index, line in enumerate(os.popen(command)):

            if line.startswith('#CHROM'):
                individuals_in_vcffile = line.strip().split()[9:]

            if not line.startswith('#'):

                chrom, pos, _, ref_allele, alt_allele = line.strip().split()[0:5]
                pos = int(pos)
                genotypes = [x.split(':')[0] for x in line.strip().split()[9:]]

                for original_genotype, individual in zip(genotypes, individuals_in_vcffile):
                    ref_count = original_genotype.count('0')
                    alt_count = original_genotype.count('1')     
                    genotype = convert_to_bases(original_genotype, ref_allele, alt_allele)   #ref_allele * ref_count + alt_allele * alt_count


                    if ancestralfile is not None:
                        ancestral_base = ancestral_allele[pos-1]
                        if ancestral_base in [ref_allele, alt_allele]:

                            derived_count = genotype.count(alt_allele) if ancestral_base == ref_allele else genotype.count(ref_allele)
                            if derived_count > 0:
                                list_of_obs[individual].append([chrom, pos, ancestral_base, genotype])

                    else:
                        # If no ancestral information is provided only include heterozygous variants
                        if alt_count * ref_count > 0:
                            list_of_obs[individual].append([chrom, pos, ancestral_base, genotype])
            

                if index % 100000 == 0:
                    print(f'at line {index} at chrom {chrom} and position {pos}')


    # Write output files
    print('\n\nSummary:')
    Make_folder_if_not_exists(outprefix)
    for individual in ingroup_individuals.split(','):
        summary_counter = defaultdict(int)
        with open(f'{outprefix}.{individual}.txt','w') as out:
            print('chrom', 'pos', 'ancestral_base', 'genotype', sep = '\t', file = out)

            for values in list_of_obs[individual]:
                chrom, pos, ancestral_base, genotype = values
                print(chrom, pos, ancestral_base, genotype, sep = '\t', file = out)

                if len(set(genotype)) == 1:
                    summary_counter['homozygous'] += 1
                else:
                    summary_counter['heterozygous'] += 1

        het = summary_counter['heterozygous']
        hom = summary_counter['homozygous']
        total = het + hom
        print(f'{individual} had {total} variants. {hom} were homozygous and {het} were heterozygous')


    # Clean log files generated by vcf and bcf tools
    clean_files('out.log')


