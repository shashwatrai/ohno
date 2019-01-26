def append_to_do(task):
	task='\n'+task
	file1 = open('to_do_list.txt', 'a+')
	file1.write(task)
	file1.close()
def delete_to_do(task):
	file2=open('to_do_list.txt','r')
	lines=file2.readlines()
	file2.close()
	file2=open('to_do_list.txt','w+')
	for line in lines:
		if line!=(task+'\n'):
			file2.write(line)
	file2.close()
def get_to_do_list_from_file():
	file3=open('to_do_list.txt','r')
	list_fetch=file3.readlines()
	return list_fetch
