 def main(mode, args):
	reads = read(args.input_path)
	mappings, t_index = prepare(reads, args)
	solutions = {}
	pool = new_threadpool()
	for id in range(0, mappings.ids):
		s = pool.new_thread(task(id, mappings, t_index, mode, args))
		solutions.union(s)
	pool.join()
	output_to(solutions, args.output_path)
	
def task(id, mappings, t_index, candidates, mode, args):
	candidates = search(id, mappings, t_index, mode, args)
	solutions = verify(candidates, mappings, args)
	return solutions
 
def search(id, mappings, t_index, candidates, mode, args):
	candidates = {}
	pattern = mappings.get_pattern(id)
	blocks = mode.get_block_sizes(pattern, args)
	for i in range(0, blocks):
		sb = blocks[i:]
		c = t_index.generate_candidates(id, sb, mappings, pattern, mode, args)
		candidates = candidates.union(c)
	return candidates
 
def verify(id, mappings, t_index, candidates, mode, args):
	solutions = {}
	for c in candidates:
		errs_allowed = errs_allowed_for(c, mappings, args)
		if args.hamming_mode == True:
			errs = hamming_distance(c, mappings, args)
		else:
			errs = edit_distance(c, mappings, args)
		if errs <= errs_allowed:
			solutions.add(convert_to_solution(c, mappings))
	return solutions
