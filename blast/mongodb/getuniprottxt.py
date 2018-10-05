import functions

if not os.path.exists("uniprotData"):
	os.makedirs("uniprotData")
functions.getUniprot()
