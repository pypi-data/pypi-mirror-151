import numpy as np
from numba import njit
import math

from helper_functions import logoutput, Make_HMM_parameters, find_runs, Make_folder_if_not_exists

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# HMM functions
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------

def Emission_probs_poisson(emissions, observations, weights, mutrates):
    n = len(observations)
    n_states = len(emissions)
    
    # observations values
    fractorials = np.zeros(n)
    for i, obs in enumerate(observations):
        fractorials[i] = math.factorial(obs)

    probabilities = np.zeros( (n, n_states) ) 
    for state in range(n_states): 
        probabilities[:,state] = (np.exp( - emissions[state] * weights * mutrates) *  ((emissions[state] * weights * mutrates )**observations )) / fractorials

    return probabilities



@njit
def fwd_step(alpha_prev, E, trans_mat):
    alpha_new = (alpha_prev @ trans_mat) * E
    n = np.sum(alpha_new)
    return alpha_new / n, n

@njit
def forward(probabilities, transitions, init_start):

    n = len(probabilities)
    forwards_in = np.zeros( (n, len(init_start)) ) 
    scale_param = np.ones(n)

    for t in range(n):
        if t == 0:
            forwards_in[t,:]=  init_start  * probabilities[t,:]
            scale_param[t] = np.sum( forwards_in[t,:])
            forwards_in[t,:] = forwards_in[t,:] / scale_param[t]
        else:
            forwards_in[t,:], scale_param[t] =  fwd_step(forwards_in[t-1,:], probabilities[t,:], transitions) 

    return forwards_in, scale_param
    

@njit
def bwd_step(beta_next, E, trans_mat, n):
    beta = (trans_mat * E) @ beta_next
    return beta / n

@njit
def backward(emissions, transitions, scales):
    n, n_states = emissions.shape
    beta = np.ones((n, n_states))
    for i in range(n - 1, 0, -1):
        beta[i - 1,:] = bwd_step(beta[i,:], emissions[i,:], transitions, scales[i])
    return beta


def GetProbability(starting_probabilities, transitions_matrix, emissions_matrix, weights, obs, mutrates):

    emissions = Emission_probs_poisson(emissions_matrix, obs, weights, mutrates)
    forward_probs, scales = forward(emissions, transitions_matrix, starting_probabilities)
    forward_probility_of_obs = np.sum(np.log(scales))

    return forward_probility_of_obs


def TrainBaumWelsch(starting_probabilities, transitions_matrix, emissions_matrix, weights, obs, mutrates):
    """
    Trains the model once, using the forward-backward algorithm. 
    """

    n_states = len(starting_probabilities)

    emissions = Emission_probs_poisson(emissions_matrix, obs, weights, mutrates)
    forward_probs, scales = forward(emissions, transitions_matrix, starting_probabilities)
    backward_probs = backward(emissions, transitions_matrix, scales)

    # Update emission
    new_emissions_matrix = np.zeros((n_states))
    for state in range(n_states):
        top = np.sum(forward_probs[:, state] * backward_probs[:, state] * obs)
        bottom = np.sum(forward_probs[:, state] * backward_probs[:, state] * (weights * mutrates) )
        new_emissions_matrix[state] = top/bottom


    # Update starting probs
    posterior_probs = forward_probs * backward_probs
    normalize = np.sum(posterior_probs)
    new_starting_probabilities = np.sum(posterior_probs, axis=0)/normalize 


    # Update Transition probs 
    new_transitions_matrix =  np.zeros((n_states, n_states))
    for state1 in range(n_states):
        for state2 in range(n_states):
            new_transitions_matrix[state1,state2] = np.sum( forward_probs[:-1,state1]  * transitions_matrix[state1, state2] * emissions[1:,state2] * backward_probs[1:,state2] / scales[1:] )

    new_transitions_matrix /=  new_transitions_matrix.sum(axis=1)[:,np.newaxis]


    return (new_starting_probabilities, new_transitions_matrix, new_emissions_matrix) 


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Train
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def TrainModel(obs, mutrates, weights, state_names, transitions, emissions_matrix, starting_probabilities, outfile):

    print('-' * 40)
    print('Selected parameters')
    print('> State names:', state_names)
    print('> Starting_probabilities:', starting_probabilities)
    print('> Transition matrix:')
    print(transitions)
    print('> Emission values:',emissions_matrix)   
    print()
    print('> number of obs:', len(obs))
    print('> total callability:', round(np.sum(weights) / len(obs),2) )
    print('> average mutation rate per bin:', round(np.sum(mutrates * weights) / np.sum(weights), 2) )
    print('> Output is',outfile) 
    print('-' * 40)

    epsilon = 1e-4

    previous_loglikelihood = GetProbability(starting_probabilities, transitions, emissions_matrix, weights, obs, mutrates)
    logoutput(emissions_matrix, previous_loglikelihood, transitions, starting_probabilities, 0)
    
    for i in range(1,1000):
        starting_probabilities, transitions, emissions_matrix = TrainBaumWelsch(starting_probabilities, transitions, emissions_matrix, weights, obs, mutrates)
        new_loglikelihood = GetProbability(starting_probabilities, transitions, emissions_matrix, weights, obs, mutrates)
        logoutput(emissions_matrix, new_loglikelihood, transitions, starting_probabilities, i)

        if new_loglikelihood - previous_loglikelihood < epsilon:       
            break 

        previous_loglikelihood = new_loglikelihood

    # Write the optimal parameters
    Make_HMM_parameters(state_names, starting_probabilities, transitions, emissions_matrix, outfile)

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
# Decode
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------
def DecodeModel(obs, chroms, starts, variants, mutrates, weights, state_names, transitions, emissions_matrix, starting_probabilities, output, window_size, decode_per_bin):
    
    print('-' * 40)
    print('Selected parameters')
    print('> State names:', state_names)
    print('> Starting_probabilities:', starting_probabilities)
    print('> Transition matrix:')
    print(transitions)
    print('> Emission values:',emissions_matrix)   
    print()
    print('> number of obs:', len(obs), '. Number of snps = ', sum(obs))
    print('> total callability:', round(np.sum(weights) / len(obs),2) )
    print('> average mutation rate per bin:', round(np.sum(mutrates * weights) / np.sum(weights), 2) )
    print('> Output is',output) 
    print('-' * 40)


    # Posterior decode the file
    emissions = Emission_probs_poisson(emissions_matrix, obs, weights, mutrates)
    forward_probs, scales = forward(emissions, transitions, starting_probabilities)
    backward_probs = backward(emissions, transitions, scales)

    post_seq = (forward_probs * backward_probs).T

    # write summary file 
    if not decode_per_bin:
        Make_folder_if_not_exists(output)
       
        with open(output,'w') as out: 
            out.write('chrom\tstart\tend\tlength\tstate\tsnps\tmean_prob\n')

            for (chrom, chrom_start_index, chrom_length_index) in find_runs(chroms):

                state_with_highest_prob = np.argmax(post_seq[:,chrom_start_index:chrom_start_index + chrom_length_index-1], axis = 0)

                for (state, start_index, length_index) in find_runs(state_with_highest_prob):

                    start_index = start_index + chrom_start_index
                    end_index = start_index + length_index

                    genome_start = starts[start_index]
                    genome_end = starts[start_index + length_index - 1]
                    genome_length =  length_index * window_size

                    snp_counter = np.sum(obs[start_index:end_index])
                    mean_prob = np.mean(post_seq[state, start_index:end_index])

                    print(chrom, genome_start, genome_end, genome_length, state_names[state], snp_counter, round(mean_prob, 5), sep = '\t', file = out)



    # write posterios prob for each bin (if specified)    
    if decode_per_bin:

        Make_folder_if_not_exists(output)
        with open(output,'w') as out:
            out.write('chrom\tstart\tobservations\tMostlikely\t{}\tvariants\n'.format('\t'.join(state_names)))
            state_with_highest_prob = np.argmax(post_seq, axis = 0)
            for index, (chrom, start_position, variant_in_bin, obs_in_bin) in enumerate(zip(chroms, starts, variants, obs)):
                print(chrom, index * window_size, obs_in_bin, state_names[state_with_highest_prob[index]], '\t'.join([str(round(val,4)) for val in post_seq[:, index]]), variant_in_bin, sep = '\t', file =  out)

