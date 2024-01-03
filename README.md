# PORTAMENTO 

This is a complete rewrite of my old project Portamento, designed for my Software Engineering bachelor's thesis project in 2021.

*Portamento: Machine Learning for music cataloguing and a three-dimensional interface to highlight its inherent nuances.*
Read the thesis (in italian): [thesis](https://github.com/nicoloddo/PORTAMENTO/blob/master/THESIS.pdf)


Portamento is a music cataloguing software that uses a selfmade mod of the BIRCH algorithm to cluster a database of tracks. The parameters of each song are withdrawn from Spotify's audio analysis databases. The interface is done using the Unity Engine with an approach similar to videogames that obtains an interactive exploration of the clustering tree hierarchy.
The backend is written in Python, while the frontend is written in C#.

[![Watch the video](https://i.imgur.com/wOLEDrZ.jpg)](https://youtu.be/aSUIdFPvFPQ)
This video shows the functioning of the Beta version.

Database references:
1. **[Spotify](https://developer.spotify.com/documentation/web-api/reference/)**, from which I get the tracks' metadata and analysis.
2. **[MusicBrainz](https://musicbrainz.org/)**, additional informations about the tracks (*to be implemented in future developments*).

## Commands
"WASD": Forward and lateral movement\
"Space": Up movement
"Shift": Down movement
Mouse: Orientation

"m": Open map\
"f": Open cluster menu

"r": Look at menu-selected cluster\
"x": Look towards x axis - "left-ctrl + x": look towards negative x axis"\
"c": Look towards y axis - "left-ctrl + c": look towards negative y axis"\
"z": Adjust orientation to be parallel to ground

## Frontend
Written in C# on the **Unity Engine**, the interface plays a very big role in the project as it follows one of the main ideas behind it by trying to highlight the actual impossibility to reduce music to a discreet number of clusters inferior to the number of the songs. It provides in fact a way to interactively explore a tree structure of clusters in which the root consist of the entire database, while the leaves are actually every sample (in that case song) of the database. This is as image of the idea that, at the highest level of detail, every song constitute a genre by itself. Moreover, the clustering parameters and weights are highly tweakable by the user to satisfy every user-specific need of categorization.

The user will be able to move inside a 3D space in which every cluster is located at specific 3 coordinates chosen from all its parameters. These 3 parameters are in fact the meaning given to the 3 axis of the space and can be modified by the user itself. It is also possible to go inside a cluster, thus going down in the tree hierarchy. By entering a cluster the user will see a totally similar scene but with the clusters that belongs to the new node of the hierarchy in which the user is now located.

## Backend
The heart of the software consists in the scripts written in Python, runned from the interface. These provide the data retrieval methods Spotify's API and the actual clusterization of the database.

## Scheme

### Nomenclature
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Nomenclature%202%20_2.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Nomenclature%202.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Nomenclature.png)

### 1.0
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Portamento%201.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Dataset%201.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Dataset%201.0%20_2.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Backend%201.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Structure%201.0%20-%20Database%20Fetch.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Structure%201.0%20-%20Tree%20Navigator.png)

### 1.1
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Portamento%201.1.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Backend%201.1.png)

### 2.0
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Portamento%202.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Dataset%202.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Backend%202.0.png)