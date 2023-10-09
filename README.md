# Groupchat analyzer of Wechat
## General Idea
our basic intention is to generate a simple user profile
## Selected dataset
simplifyweibo_4_moods dataset : A Chinese dataset with 360k different sort of emotions.
## Methods discussed
Generally we tend to implement a neural network to handle our question. We want to contain as much valid data as possible, since the Chinese text is beyond complicated than any other in the world.
We do hope to implement both Coarse-grained and Fine-grained sentiment analysis 
## How to inplement this network
Due to the special policy of privacy of Wechat, till now it's not yet convinient to export the groupchat history on devices other than IOS. Thus please  implement app on www.i4.cn to export the groupchat history.
After that, please specify the file /preprocess/txt2csv as requested
