# import gzip
import gensim

# import logging

model = gensim.models.KeyedVectors.load_word2vec_format('/home/christinejyeon/GoogleNews-vectors-negative300.bin',
                                                        binary=True, unicode_errors='ignore')
import numpy as np
import pandas as pd

## Finding about the model
len(list(model.vocab))

######## THROWING TAGS IN WORD2VEC

tag_df = pd.read_excel('/home/christinejyeon/tag_original.xlsx', header=None)
tag_df.head()
# tag_df = tag_df[1]
taglist = tag_df[1].values.tolist()

tagvectors = model["baseball"]
# tagvectors
tagvectors = pd.DataFrame(data=np.float32(tagvectors))
tagvectors.columns = ['baseball']

for i in range(2, len(taglist) + 1):
    try:
        embedding_vector = model[taglist[i]]
        vdf = pd.DataFrame(data=np.float32(embedding_vector))
        vdf.columns = [taglist[i]]
        tagvectors = pd.concat([tagvectors.reset_index(drop=True), vdf.reset_index(drop=True)], axis=1)
    except KeyError:
        print("not in vocabulary")

# model's shape is [300, ]
# tagvectors.shape -> (300,3405)


######## THROWING TGM CONCEPTS IN WORD2VEC

tgm_df = pd.read_excel('/home/christinejyeon/tgmdescriptors.xlsx')
tgm_df.head()
# tgm_df = tgm_df['Description']

tgmlist = tgm_df['Description'].values.tolist()

tgmvectors = model["Abbeys"]
# tagvectors
tgmvectors = pd.DataFrame(data=np.float32(tgmvectors))
tgmvectors.columns = ['Abbeys']

for i in range(20, len(tgmlist) + 1):
    try:
        embedding_vector = model[tgmlist[i]]
        vdf = pd.DataFrame(data=np.float32(embedding_vector))
        vdf.columns = [tgmlist[i]]
        tgmvectors = pd.concat([tgmvectors.reset_index(drop=True), vdf.reset_index(drop=True)], axis=1)
    except KeyError:
        print("not in vocabulary")

# model's shape is [4629,]
# final shape: (300, 4629)


#### Save both vector datasets
# tagvectors.to_csv("/home/christinejyeon/tagvectors.csv",sep='\t', encoding='utf-8')
# tgmvectors.to_csv("/home/christinejyeon/tgmvectors.csv",sep='\t', encoding='utf-8')
# tagvectors.to_pickle("/home/christinejyeon/tagvectors.pkl")
# tgmvectors.to_pickle("/home/christinejyeon/tgmvectors.pkl")


###### Working on clustering

from matplotlib import pyplot as plt
from scipy.cluster.hierarchy import dendrogram, linkage

from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as shc

######### switching rows and columns
tagvectors_horizontal = tagvectors.T
tagvectors_horizontal_sp = tagvectors_horizontal.copy()
tagvectors_horizontal.index.name = 'tagname'
tagvectors_horizontal.reset_index(inplace=True)

################### DRAWING DENDROGRAM
Z = linkage(tagvectors_horizontal_sp, 'ward')

# set cut-off to 150
max_d = 7.08                # max_d as in max_distance

plt.figure(figsize=(25, 25))
plt.title('Tag Clustering Dendrogram')
plt.xlabel('vectors')
plt.ylabel('distance')
dendrogram(
    Z,
    truncate_mode='lastp',  # show only the last p merged clusters
    p=150,                  # Try changing values of p
    leaf_rotation=90.,      # rotates the x axis labels
    leaf_font_size=8.,      # font size for the x axis labels
)
plt.axhline(y=max_d, c='k')
plt.show()
plt.savefig('/home/christinejyeon/dendrogram_1219.png')

# calculate full dendrogram for 50

#plt.figure(figsize=(25, 10))
#plt.title('Iris Hierarchical Clustering Dendrogram')
#plt.xlabel('Species')
#plt.ylabel('distance')
#dendrogram(
#    Z,
#    truncate_mode='lastp',  # show only the last p merged clusters
#    p=50,                  # Try changing values of p
#    leaf_rotation=90.,      # rotates the x axis labels
#    leaf_font_size=8.,      # font size for the x axis labels
#)
#plt.axhline(y=max_d, c='k')
#plt.savefig("/home/christinejyeon/dendrogram_2.png")
#plt.show()

################# AGGLOMERATIVE CLUSTERING ###################
from sklearn.cluster import AgglomerativeClustering

cluster = AgglomerativeClustering(n_clusters=12, affinity='euclidean', linkage='ward')
cluster.fit_predict(tagvectors_horizontal_sp)
cluster = pd.DataFrame({'tagname':tagvectors_horizontal.tagname.tolist() , 'cluster':cluster.fit_predict(tagvectors_horizontal_sp)})
cluster.to_csv("/home/christinejyeon/cluster_1219.csv", sep="\t", encoding="utf-8")
cluster.to_pickle("/home/christinejyeon/cluster_1219.pkl")


################# Finding the representative value for each clusters ###############
# First cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==0]
temp = temp["tagname"].tolist()
cluster_first = tagvectors_horizontal.copy()
cluster_first = cluster_first[cluster_first["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_first)):
    try:
        for j in range(0, len(cluster_first)):
            temp = cluster_first.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 492
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_first = cluster_first.iloc[355:356]

# Second cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==1]
temp = temp["tagname"].tolist()
cluster_second = tagvectors_horizontal.copy()
cluster_second = cluster_second[cluster_second["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_second)):
    try:
        for j in range(0, len(cluster_second)):
            temp = cluster_second.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 1027
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_second = cluster_second.iloc[755:756]


# Third cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==2]
temp = temp["tagname"].tolist()
cluster_third = tagvectors_horizontal.copy()
cluster_third = cluster_third[cluster_third["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_third)):
    try:
        for j in range(0, len(cluster_third)):
            temp = cluster_third.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 216
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_third = cluster_third.iloc[112:113]


# Fourth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==3]
temp = temp["tagname"].tolist()
cluster_fourth = tagvectors_horizontal.copy()
cluster_fourth = cluster_fourth[cluster_fourth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_fourth)):
    try:
        for j in range(0, len(cluster_fourth)):
            temp = cluster_fourth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 297
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_fourth = cluster_fourth.iloc[232:233]


# Fifth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==4]
temp = temp["tagname"].tolist()
cluster_fifth = tagvectors_horizontal.copy()
cluster_fifth = cluster_fifth[cluster_fifth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_fifth)):
    try:
        for j in range(0, len(cluster_fifth)):
            temp = cluster_fifth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 340
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_fifth = cluster_fifth.iloc[66:67]


# Sixth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==5]
temp = temp["tagname"].tolist()
cluster_sixth = tagvectors_horizontal.copy()
cluster_sixth = cluster_sixth[cluster_sixth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_sixth)):
    try:
        for j in range(0, len(cluster_sixth)):
            temp = cluster_sixth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 97
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_sixth = cluster_sixth.iloc[17:18]


# Seventh cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==6]
temp = temp["tagname"].tolist()
cluster_seventh = tagvectors_horizontal.copy()
cluster_seventh = cluster_seventh[cluster_seventh["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_seventh)):
    try:
        for j in range(0, len(cluster_seventh)):
            temp = cluster_seventh.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 136
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_seventh = cluster_seventh.iloc[12:13]


# Eighth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==7]
temp = temp["tagname"].tolist()
cluster_eighth = tagvectors_horizontal.copy()
cluster_eighth = cluster_eighth[cluster_eighth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_eighth)):
    try:
        for j in range(0, len(cluster_eighth)):
            temp = cluster_eighth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 131
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_eighth = cluster_eighth.iloc[117:118]


# Ninth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==8]
temp = temp["tagname"].tolist()
cluster_ninth = tagvectors_horizontal.copy()
cluster_ninth = cluster_ninth[cluster_ninth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_ninth)):
    try:
        for j in range(0, len(cluster_ninth)):
            temp = cluster_ninth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 136
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_ninth = cluster_ninth.iloc[81:82]


# Tenth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==9]
temp = temp["tagname"].tolist()
cluster_tenth = tagvectors_horizontal.copy()
cluster_tenth = cluster_tenth[cluster_tenth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_tenth)):
    try:
        for j in range(0, len(cluster_tenth)):
            temp = cluster_tenth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 100
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_tenth = cluster_tenth.iloc[3:4]


# Eleventh cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==10]
temp = temp["tagname"].tolist()
cluster_eleventh = tagvectors_horizontal.copy()
cluster_eleventh = cluster_eleventh[cluster_eleventh["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_eleventh)):
    try:
        for j in range(0, len(cluster_eleventh)):
            temp = cluster_eleventh.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 228
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_eleventh = cluster_eleventh.iloc[53:54]


# Twelfth cluster
temp = cluster.copy()
temp = temp.loc[temp["cluster"]==11]
temp = temp["tagname"].tolist()
cluster_twelfth = tagvectors_horizontal.copy()
cluster_twelfth = cluster_twelfth[cluster_twelfth["tagname"].isin(temp)]

temp_cosinesimilarity = 0
temp_cosinelist = []
for i in range(0, len(cluster_twelfth)):
    try:
        for j in range(0, len(cluster_twelfth)):
            temp = cluster_twelfth.copy()
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp.iloc[j].as_matrix(columns=temp.columns[1:])
            temp_cosinesimilarity = temp_cosinesimilarity + (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
        temp_cosinesimilarity = temp_cosinesimilarity / 205
        temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinesimilarity = 0
    except KeyError:
        print(":(")
temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
temp_cosinelist.columns = ["similarities"]
temp_cosinelist.loc[temp_cosinelist['similarities'].idxmax()]

cluster_twelfth = cluster_twelfth.iloc[159:160]

# saving the representatives
cluster_first.to_pickle("/home/christinejyeon/cluster_first.pkl")
cluster_second.to_pickle("/home/christinejyeon/cluster_second.pkl")
cluster_third.to_pickle("/home/christinejyeon/cluster_third.pkl")
cluster_fourth.to_pickle("/home/christinejyeon/cluster_fourth.pkl")
cluster_fifth.to_pickle("/home/christinejyeon/cluster_fifth.pkl")
cluster_sixth.to_pickle("/home/christinejyeon/cluster_sixth.pkl")
cluster_seventh.to_pickle("/home/christinejyeon/cluster_seventh.pkl")
cluster_eighth.to_pickle("/home/christinejyeon/cluster_eighth.pkl")
cluster_ninth.to_pickle("/home/christinejyeon/cluster_ninth.pkl")
cluster_tenth.to_pickle("/home/christinejyeon/cluster_tenth.pkl")
cluster_eleventh.to_pickle("/home/christinejyeon/cluster_eleventh.pkl")
cluster_twelfth.to_pickle("/home/christinejyeon/cluster_twelfth.pkl")


########### Calculating each cluster's similarity with each tgm vector

## TGM vectors switch rows with columns
tgmvectors_horizontal = tgmvectors.T
tgmvectors_horizontal_sp = tgmvectors_horizontal.copy()
tgmvectors_horizontal.index.name = 'tgmname'
tgmvectors_horizontal.reset_index(inplace=True)
tgmvectors_horizontal = tgmvectors_horizontal.copy()

# tgmvectors_horizontal.to_csv("/home/christinejyeon/tgmvectors_horizontal.csv", sep="\t", encoding="utf-8")
# tgmvectors_horizontal.to_pickle("/home/christinejyeon/tgmvectors_horizontal.pkl")

## binding the representative vectors of each cluster
ultimate_rep = cluster_first.copy()
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_second), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_third), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_fourth), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_fifth), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_sixth), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_seventh), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_eighth), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_ninth), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_tenth), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_eleventh), ignore_index=True)
ultimate_rep = ultimate_rep.append(pd.DataFrame(data = cluster_twelfth), ignore_index=True)

# ultimate_rep.to_csv("/home/christinejyeon/ultimate_rep.csv", sep="\t", encoding="utf-8")
# ultimate_rep.to_pickle("/home/christinejyeon/ultimate_rep.pkl")

## calculating similarities
temp = ultimate_rep.copy()
temp1 = tgmvectors_horizontal.copy()
temp_cosinelist=[]

for j in range(0, 4629):
    vec1 = temp.iloc[0].as_matrix(columns=temp.columns[1:])
    vec2 = temp1.iloc[j].as_matrix(columns=temp1.columns[1:])
    temp_cosinesimilarity = (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    temp_cosinelist.append(temp_cosinesimilarity)
tag_tgm_similarity = pd.DataFrame(data=np.float32(temp_cosinelist))
# temp_cosinelist.columns = ["similarities"]

for i in range(1, 12):
    try:
        temp_cosinelist = []
        for j in range(0, 4629):
            vec1 = temp.iloc[i].as_matrix(columns=temp.columns[1:])
            vec2 = temp1.iloc[j].as_matrix(columns=temp1.columns[1:])
            temp_cosinesimilarity = (np.sum(vec1 * vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
            temp_cosinelist.append(temp_cosinesimilarity)
        temp_cosinelist = pd.DataFrame(data=np.float32(temp_cosinelist))
        temp_cosinelist.columns = [i]
        tag_tgm_similarity = pd.concat([tag_tgm_similarity.reset_index(drop=True), temp_cosinelist], axis=1)
    except KeyError:
        print(":(")

tag_tgm_similarity.to_csv("/home/christinejyeon/tag_tgm_similarity.csv",sep='\t', encoding='utf-8')
tag_tgm_similarity.to_pickle("/home/christinejyeon/tag_tgm_similarity.pkl")

