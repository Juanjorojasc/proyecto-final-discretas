"""
Author:Oscar Vargas Pabon

################################################  case format output/input
First a line with a number (amount of cases)
<t>
Then, for each test case
<n=parties> <p=policies> <percentage>
<am_1> <am_2> ... <am_n>
<A_{1,1}> <A_{1,2}> ... <A_{1,p}>
...
<A_{n,1}> <A_{n,2}> ... <A_{n,p}>
Where each $<A_{i,j}>\\in\\{-1,0,1\\}$ represents the stance of party $i$ regarding policy $j$,
	each $<am_i>\\in\\mathbb{N}_{>0}$ represents the amount of seats the $i$th party has.

################################################  answer format output
First a line with a number (amount of cases)
<t>
Then, for each test case
<policy_1> <policy_2> .. <policy_p>
Where each $<policy_i>\\in\\{-1,1\\}$ meaning, the decision made by the solver regarding the
	$i$th policy. If they are all zero, it means the answer is impossible.

################################################  compare format output
First a line with a number (amount of cases)
<t>
<answer_1>
<answer_2>
...
<answer_t>

Where each $<answer_i>\\in\\{"YES","NO"\\}$ meaning, if the case was possible or not.

################################################  dnf format output
First a line with a number (amount of cases)
<t>
<dnf_1>
<dnf_2>
...
<dnf_t>

Where $<dnf_i>$ is a string that has the output of the function "generate_dnf" in the $i$th case.

Interface:
	-s=<number>  |-> the seed for the pseudo-random generator (s=random by default)
	-c=<string>  |-> the case type. Check Case_code to see what it means
	-c=t,n,p,per |-> Charges this custom test into the code (iterations,parties,policies,percentage)
	-print_case=<file> |-> outputs the case in the aforementioned format
	-read_case=<file>  |-> tests the model with a case (it is not compatible with -c and -s and will overwrite it)
	-print_ans=<file>  |-> outputs the assignation in the aforementioned format through stdout
	-print_cmp=<file>  |-> outputs 'YES' if it found an answer. 'NO' if it didnt
	-print_dnf=<file>  |-> outputs the DNF of the cases
NOTES: not adding the =<file> results in outputing to stdout
"""

import sys,time,random
sys.setrecursionlimit(10**9+333)
import solver ## the one we will implement

##############################################################################################################
########################################### Random generation stuff ##########################################
##############################################################################################################
MIN_SEAT,MAX_SEAT=1,20
gen_vec     =lambda n,mn,mx:[random.randint(mn,mx) for _ in range(n)]
gen_mat     =lambda n,m,mn,mx:[gen_vec(m,mn,mx) for _ in range(n)]
gen_seats   =lambda n,mn=MIN_SEAT,mx=MAX_SEAT:gen_vec(n,mn,mx)
gen_policies=lambda n,m:gen_mat(n,m,-1,1)
##############################################################################################################
########################################### Check answer stuff ###############################################
##############################################################################################################
def check_result(seats:list[int],policies:list[list[int]],percentage:float,decision:list[int] )->bool:
	res=len(decision)==len(policies[0]) and decision.count(0) in {0,len(decision)}
	if(decision!=[0 for _ in range(len(decision))] and res):
		gov_seats=0
		for i in range(len(seats)):
			party=policies[i]
			gov_party=True
			for j in range(len(party)):
				gov_party=gov_party and (party[j]==0 or party[j]==decision[j])
			if(gov_party):gov_seats+=seats[i]#1e-12 is for precision errors 
		res=gov_seats+1e-12>=sum(seats)*percentage
	return res
##############################################################################################################
########################################### interface and main ###############################################
##############################################################################################################
## (iterations,party_amount,policy_amount,percentage)
Case_code={
	"test-0":(2,3,4,0.5),
	"test-1":(2,10,10,0.7),
	"test-2":(2,5,20,1),
	"test-3":(10,18,18,0.7),
	"obj-0":(10,16,16,0.5),
	"obj-1":(10,24,24,0.5),
	"obj-2":(10,40,40,0.5),
	"bonus-0":(10,77,77,0.5),
	"bonus-1":(10,100,100,0.5),
	}

def main():
	s=time.time()
	t,n,p,perc=Case_code["test-0"]
	print_case=""
	read_case =""
	print_ans =""
	print_cmp =""
	print_dnf =""
	for i in range(1,len(sys.argv)):
		nm=sys.argv[i]
		if( nm[:11]=="-print_case"):
			if(nm=="-print_case"):print_case="stdout"
			else: print_case=nm[12:]
		elif(nm[:10]=="-read_case"):
			if(nm=="-read_case"):read_case="stdin"
			else: read_case =nm[11:]
		elif(nm[:10]=="-print_ans"):
			if(nm=="-print_ans"):print_ans="stdout"
			else: print_ans =nm[11:]
		elif(nm[:10]=="-print_cmp"):
			if(nm=="-print_cmp"):print_cmp="stdout"
			else: print_cmp =nm[11:]
		elif(nm[:10]=="-print_dnf"):
			if(nm=="-print_dnf"):print_dnf="stdout"
			else: print_dnf =nm[11:]
		elif(nm[:3]=="-s="):s=int(nm[3:])
		elif(nm[:3]=="-c="):
			nm=nm[3:]
			if(","in nm):
				nm=nm.split(",")
				t,n,p=list(map(int,nm[:3]))
				perc=float(nm[3])
			else:
				assert(nm in Case_code)
				t,n,p,perc=Case_code[nm]
		else: assert(False),"Error: flag |%s| not recognized."%(nm)
	random.seed(s)
	
	all_ans=[]
	all_time:int=0
	all_case=[]
	all_dnf=[]

	if(read_case):
		if(read_case=="stdin"): ifile=sys.stdin
		else: ifile=open(read_case,"r")
		t=int(ifile.readline().strip())
		print("Cases read from: <%s>.\n"%(read_case),file=sys.stderr)
	else: print("Cases ran with seed: <%d>.\n"%(s),file=sys.stderr)
	for _ in range(t):
		if(read_case):
			n,p,perc=ifile.readline().split(" ")
			n=int(n)
			p=int(p)
			perc=float(perc)

			seats=list(map(int,ifile.readline().split(" ")))
			policy=[]
			for i in range(n):
				policy.append( list(map(int,ifile.readline().split(" "))) )
		else:
			seats =gen_seats(n)
			policy=gen_policies(n,p)
		all_case.append((seats,policy,perc))

		system=solver.PoliticalSAT(seats,policy)

		init_time=time.time_ns()
		decision=system.solve_stability(perc)
		all_time+=time.time_ns()-init_time

		assert(check_result(seats,policy,perc,decision))

		all_dnf.append(system.generate_dnf())
		all_ans.append(decision)
	if(read_case and read_case!="stdin"): ifile.close()
	if(print_case):
		def print_the_case(file):
			nonlocal all_case
			file.write("%d\n"%(len(all_case)))
			for seats,policy,perc in all_case:
				file.write("%d %d %f\n"%(len(seats),len(policy[0]),perc) )
				file.write(" ".join(map(str,seats)))
				file.write("\n")
				for party in policy:
					file.write(" ".join(map(str,party)) )
					file.write("\n")
		if(print_case=="stdout"):
			print_the_case(sys.stdout)
		else:
			with open(print_case,"w") as file:
				print_the_case(file)
	if(print_ans):
		def print_the_ans(file):
			nonlocal all_ans
			file.write("%d\n"%(t))
			for decision in all_ans:
				file.write(" ".join(map(str,decision)))
				file.write("\n")
		if(print_ans=="stdout"): print_the_ans(sys.stdout)
		else:
			with open(print_ans,"w") as file:
				print_the_ans(file)
	if(print_cmp):
		print_the_cmp="\n".join(list(map(lambda x:"NO" if x[0]==0 else "YES",  all_ans)))
		if(print_cmp=="stdout"):print(print_the_cmp)
		else:
			with open(print_cmp,"w") as file:
				file.write(print_the_cmp)
	if(print_dnf):
		print_the_dnf="\n".join(all_dnf)
		if(print_dnf=="stdout"):print(print_the_dnf)
		else:
			with open(print_dnf,"w") as file:
				file.write(print_the_dnf)
	print("\nFinished. The total time of the solver was <%f> miliseconds.\n"%(all_time/10**6))
if __name__ == '__main__':
	main()