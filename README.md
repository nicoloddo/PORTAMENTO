# PORTAMENTO 

This is a complete rewrite of my old project Portamento, designed for my Software Engineering bachelor's thesis project in 2021. The goal of the rewrite is to make it available online on my website, while running the backend on AWS as a serverless architecture.

You can look at src/model for the backend.
The frontend at src/unity.

*Portamento: Machine Learning for music cataloguing and a three-dimensional interface to highlight its inherent nuances.*
Read the thesis (in italian): [thesis](https://github.com/nicoloddo/PORTAMENTO/blob/master/THESIS.pdf)


Portamento is a music cataloguing software that uses a selfmade mod of the BIRCH algorithm to cluster a database of tracks. The interface is developed using the Unity Engine, obtaining an immersive and interactive exploration of the clustering tree hierarchy.
The backend is written in Python, while the frontend is written in C#.

[![Watch the video](https://i.imgur.com/wOLEDrZ.jpg)](https://youtu.be/aSUIdFPvFPQ)
This video shows the functioning of the Beta version.
You can try yourself the current version at [nicoloddo.github.io/PORTAMENTO](https://nicoloddo.github.io/PORTAMENTO/)

Database references:
1. **[Spotify](https://developer.spotify.com/documentation/web-api/reference/)**, from which I get the tracks' metadata and analysis.
2. **[MusicBrainz](https://musicbrainz.org/)**, additional informations about the tracks (*to be implemented in future developments*).

## Commands
"WASD": Forward and lateral movement\
"Space": Up movement
"Shift": Down movement
Mouse: Orientation

"M": Open map\
"F": Open cluster menu

"E": Go to the map-selected cluster\
"X": Look towards x axis - "left-ctrl + X": look towards negative x axis"\
"C": Look towards y axis - "left-ctrl + C": look towards negative y axis"\
"Z": Adjust orientation to be parallel to ground

## Backend
The backend is written in Python and runs on AWS on a serverless architecture based on Lambdas, S3 and API Gateway. The backend handles the data retrieval from Spotify's API, the clusterization of the database and the navigation inside its structure.

## Frontend
Written in C# on the **Unity Engine**, the interface lets users explore the clusters inside a 3D universe, where they can move along 3 chosen attributes of the song (e.g. danceability, valence, energy) and enter the clusters to achieve more specificity.

## Scheme

### 1.0
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Portamento%201.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Backend%201.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Structure%201.0%20-%20Database%20Fetch.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Structure%201.0%20-%20Tree%20Navigator.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Dataset%201.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Dataset%201.0_2.png)

### 1.1
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Portamento%201.1.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Backend%201.1.png)

### 2.0
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Portamento%202.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Backend%202.0.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Dataset%202.0.png)

### Nomenclature
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Nomenclature.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Nomenclature%202.png)
![-](https://raw.githubusercontent.com/nicoloddo/PORTAMENTO/main/slides/Nomenclature%202_2.png)