import functions
table = functions.connectMongoDB('uniprot','table')
ptms = {'Phosphoserine':[],'Phosphothreonine':[],'Phosphotyrosine':[],'N6-acetyllysine':[],'Omega-N-methylarginine':[],
'N6-methyllysine':[],'N6,N6-dimethyllysine':[],'N6,N6,N6-trimethyllysine':[],'N-linked(GlcNAc)asparagine':[],
'S-palmitoylcysteine': [],'Pyrrolidonecarboxylicacid':[],'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-CterinSUMO)':[]
,'Glycyllysineisopeptide(Lys-Gly)(interchainwithG-Cterinubiquitin)':[]}
for ptm in ptms:
    result = table.find({ptm : {"$exists": True}})
    print(ptm+": ")
    print(result.count())
