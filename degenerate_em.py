import random
from operator import indexOf
model_a = "mystery_A.fprobs.txt"
model_b = "mystery_A.fprobs.txt"
model_c = "mystery_A.fprobs.txt"

def initialize_lambda_weights(lang_models):
	lambda_weights = []
	running_sum = 0.0
	for x in range(len(lang_models)):
		r = random.uniform(0,1)
		running_sum += r
		lambda_weights.append(r)
	lambda_weights = [x/running_sum for x in lambda_weights]
	print("Initializing lambdas: Weights sum to " + str(sum(lambda_weights)))
	print(lambda_weights)
	return lambda_weights

def run_em(models):
	lang_models = []
	N = 0
	for i, model in enumerate(models):
		N = len(model)
		lang_models.append([float(x) for x in open(model).readlines()])
		print("Length of model " + str(i+1) + ": " + str(N) + " and values sum to: " + \
			str(sum(lang_models[i])))
	print("N is " + str(N))
	
	lambda_weights = initialize_lambda_weights(lang_models)
	iteration = 0
	
	



if __name__ == '__main__':
	run_em((model_a,model_b,model_c))
