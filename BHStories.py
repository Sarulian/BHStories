# This contains all useful python functions for BHStories

# Returns only the first word of a series of words
def limit_one_word(user_input):

	return user_input.split()[0]


# Main function for testing
def main():

	print(limit_one_word("This is multiple words"))
	print(limit_one_word("word"))


if __name__ == "__main__":
	main()
	