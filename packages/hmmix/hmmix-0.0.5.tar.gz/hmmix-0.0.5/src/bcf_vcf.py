import os
import numpy as np
from collections import defaultdict
import sys 
from glob import glob
import json

from helper_functions import get_consensus, sortby, Make_folder_if_not_exists, get_ancestral_from_fasta, convert_to_bases, handle_individuals_input, handle_infiles, clean_files

# Check which type of input we are dealing with
def combined_files(ancestralfiles, vcffiles):

    if len(ancestralfiles) == len(vcffiles):

        if ancestralfiles == ['']:
            return [None], vcffiles
        else:
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
def make_out_group(individuals_input, bedfile, vcffiles, outputfile, ancestralfiles):

    # Get list of outgroup individuals
    outgroup_individuals = handle_individuals_input(individuals_input, 'outgroup')

    # Get a list of vcffiles and ancestral files and intersect them
    vcffiles = handle_infiles(vcffiles)
    ancestralfiles = handle_infiles(ancestralfiles)
    ancestralfiles, vcffiles  = combined_files(ancestralfiles, vcffiles)

    print('-' * 40)
    print('Selected parameters')
    print('\n> Outgroup individuals:', len(outgroup_individuals))
    print('First 10..')
    for i, x in enumerate(outgroup_individuals):
        print(x)
        if i > 10:
            break
    print()
    print('> Using vcf and ancestral files')
    for vcffile, ancestralfile in zip(vcffiles, ancestralfiles):
        print('vcffile:',vcffile, 'ancestralfile:',ancestralfile)
    print()    
    print('> Callability file:\n', bedfile, '\n')
    print(f'> Writing output to:\n',outputfile,'\n')
    print('-' * 40)

    Make_folder_if_not_exists(outputfile)
    outgroup_individuals = ','.join(outgroup_individuals)

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
                    if alt_count * ref_count > 0:
                        ancestral_base = ref_allele if ref_count > alt_count else alt_allele

                        # Use ancestral base info if available
                        if ancestralfile is not None:
                            ancestral_base_temp = ancestral_allele[pos-1]
                            if ancestral_base_temp in [ref_allele, alt_allele]:
                                 ancestral_base = ancestral_base_temp

                        print(chrom, pos, ref_allele_info, alt_allele_info, ancestral_base, sep = '\t', file = out)

                    # Fixed sites
                    elif alt_count * ref_count == 0:

                        ancestral_base = ref_allele if ref_count > alt_count else alt_allele
                        # Use ancestral base info if available
                        if ancestralfile is not None:
                            ancestral_base_temp = ancestral_allele[pos-1]
                            if ancestral_base_temp in [ref_allele, alt_allele]:
                                 ancestral_base = ancestral_base_temp

                        if ancestral_base == alt_allele:
                            derived_count = ref_count
                        else:
                             derived_count = alt_count

                        if derived_count > 0:
                            print(chrom, pos, ref_allele_info, alt_allele_info, ancestral_base, sep = '\t', file = out)


                    if index % 100000 == 0:
                        print(f'at line {index} at chrom {chrom} and position {pos}')

    # Clean log files generated by vcf and bcf tools
    clean_files('out.log')
    






def make_ingroup_obs(individuals_input, bedfile, vcffiles, outprefix, outgroupfile, ancestralfiles):

    # Get a list of ingroup individuals
    ingroup_individuals = handle_individuals_input(individuals_input, 'ingroup')

    # Get a list of vcffiles and ancestral files and intersect them
    vcffiles = handle_infiles(vcffiles)
    ancestralfiles = handle_infiles(ancestralfiles)
    ancestralfiles, vcffiles  = combined_files(ancestralfiles, vcffiles)

    print('-' * 40)
    print('Selected parameters')
    print('\n > Ingroup individuals:', len(ingroup_individuals))
    print('First 10')
    for i, x in enumerate(ingroup_individuals):
        print(x)
        if i > 10:
            break
    print()

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
                    genotype = convert_to_bases(original_genotype, ref_allele, alt_allele)   

                    if ancestralfile is not None:
                        # With ancestral information look for derived alleles
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



