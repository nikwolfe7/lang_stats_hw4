import copy
import random
import numpy
model_a = "mystery_A.fprobs.txt"
model_b = "mystery_B.fprobs.txt"
model_c = "mystery_C.fprobs.txt"
convergence_difference = 0.00001

def initialize_lambda_weights(lang_models):
	lambda_weights = [random.uniform(0,1) for _ in range(len(lang_models))]
	lambda_weights = normalize_weights(lambda_weights)
	print("Initializing lambdas: Weights sum to " + str(sum(lambda_weights)))
	print(lambda_weights)
	return lambda_weights

def normalize_weights(weights):
	total = sum(weights)
	return [x/total for x in weights]

def logify(stuff):
	for i in range(len(stuff)):
		if(stuff[i] == 0): stuff[i] = numpy.log(0.0000000000001)
		else: stuff[i] = numpy.log(float(stuff[i]))
	return stuff

#computes log sum of two exponentiated log numbers efficiently
def log_sum(left,right):
	if right < left:
		return left + numpy.log1p(numpy.exp(right - left))
	elif left < right:
		return right + numpy.log1p(numpy.exp(left - right))
	else:
		return left + numpy.log1p(1)

# one iteration of the EM algorithm...
def e_step(lang_models, lambda_weights, K, N):
	for j in range(len(lambda_weights)):
		update = 0.0
		for i in range(N):
			numerator = lang_models[j][i] * lambda_weights[j]
			#numerator = lang_models[j][i] + lambda_weights[j] 
			denominator = 0.0
			for k in range(K):
				denominator = denominator + (lambda_weights[k] * lang_models[k][i])
				#denominator = log_sum(denominator, (lambda_weights[k] + lang_models[k][i]))
			update = update + (numerator / denominator)
			#update = log_sum(update, (numerator - denominator))
		update = update / N
		lambda_weights[j] = update
	#return normalize_weights(lambda_weights)
	return lambda_weights

def m_step(lang_models, lambda_weights, K, N):
	likelihood_lambda = 0.0
	for i in range(N):
		inner_product = 0.0
		for k in range(K):
			word_lambda = lambda_weights[k] * lang_models[k][i]
			#word_lambda = (lambda_weights[k] + lang_models[k][i])
			inner_product += word_lambda
		likelihood_lambda += numpy.log(inner_product)
	likelihood_lambda = likelihood_lambda / N
	return likelihood_lambda

def convergence_test(L_t, L_t_plus_one):
	ratio = (L_t_plus_one - L_t)/numpy.abs(L_t_plus_one)
	print("Difference: " + str(ratio))
	return ratio <= convergence_difference
	

def run_em(models):
	lang_models = []
	N = 0
	for model in models:
		i = models.index(model)
		lang_models.append([float(x) for x in open(model).readlines()])
		N = len(lang_models[-1])
		print("Length of model " + str(i+1) + ": " + str(N) + " and values sum to: " + \
			str(sum(lang_models[i])))
	
	
	#lambda_weights = initialize_lambda_weights(lang_models)
	lambda_weights = [1.0/3, 1.0/3, 1.0/3]
	print("Initial lambda weights: " + str(lambda_weights))
	iteration = 1
	K = len(lambda_weights)
	print("N is " + str(N))
	print("K is " + str(K))
	
	#print("Logifying...")
	#lambda_weights = logify(lambda_weights)
	for model in lang_models:
		# model = logify(model)
		print("Model " + str(lang_models.index(model)) + ": " + str(model))
		
	
	# ------------------------------------- #
	# EM ALGORITHM ************************ #
	# ------------------------------------- #
	print("\nIteration " + str(iteration) + ": ")
	old_weights = copy.deepcopy(lambda_weights)
	new_weights = e_step(lang_models, lambda_weights, K, N)
	likelihood_lambda_t = m_step(lang_models, old_weights, K, N)
	likelihood_lambda_t_plus_one = m_step(lang_models, new_weights, K, N)
	print("Lambda weights for iteration "+str(iteration) + ": " + str(new_weights))
	print("Log Likelihood L(lam(t)): "+str(likelihood_lambda_t))
	print("Log Likelihood L(lam(t+1)): "+str(likelihood_lambda_t_plus_one))
					
	while not convergence_test(likelihood_lambda_t, likelihood_lambda_t_plus_one):
		iteration += 1
		print("\nIteration " + str(iteration) + ": ")
		old_weights = copy.deepcopy(lambda_weights)
		new_weights = e_step(lang_models, lambda_weights, K, N)
		likelihood_lambda_t = m_step(lang_models, old_weights, K, N)
		likelihood_lambda_t_plus_one = m_step(lang_models, new_weights, K, N)
		print("Lambda weights for iteration "+str(iteration) + ": " + str(new_weights))
		print("Log Likelihood L(lam(t)): "+str(likelihood_lambda_t))
		print("Log Likelihood L(lam(t+1)): "+str(likelihood_lambda_t_plus_one))
		
	print("Hooray! We converged!")
	

if __name__ == '__main__':
	run_em((model_a,model_b,model_c))
