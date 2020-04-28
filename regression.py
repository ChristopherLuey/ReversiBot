file = open("weights.txt","r")

text = file.readlines()

nums = []
for line in text:
	if line[0] == "[":
		line = eval(line)
		if len(line) == 1:
			nums.append(line)

for index in range(len(nums[0])):

	for listNum in range(len(nums)):
		nums[listNum][index] = str(nums[listNum][index])

		if not nums[listNum][index].find("e")==-1:

			number = nums[listNum][index].split("e")
			nums[listNum][index] = float(number[0]) * (10**float(number[1]))

		print(nums[listNum][index])

	print("-----")

file.close()