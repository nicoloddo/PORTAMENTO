using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongMenu : MonoBehaviour
{
    private const int AXIS_MULTIPLIER = 400;  // Also present in Cluster and DisplayMenu classes
    private const int COORD_MULTIPLIER = 100; // Maximum value of coordinates during display
    private const int SONGS_IN_PAGE = 11; // Number of songs in a page

    public GameObject FeaturesContainer;
    private Text _featuresLabel;
    private GameObject _player;
    private string _prevClust = "";

    void Start()
    {
        _player = GameObject.FindGameObjectWithTag("Player");
        _featuresLabel = FeaturesContainer.GetComponentInChildren<Text>();
        _featuresLabel.text = "Press a song to see its characteristics here.";
    }

    public void CreateMenu(bool isLeaf, string clusterId, List<Dictionary<string, string>> songsMeta, 
        List<Dictionary<string, float>> songsTrack, Dictionary<string, float> centroid, int page = 0)
    {
        GameObject clustButton;
        Transform[] children = gameObject.GetComponentsInChildren<Transform>();
        int numSongs = songsMeta.Count;

        if (songsMeta.Count != songsTrack.Count)
        {
            Debug.Log("In CreateMenu() songsMeta and songsTrack have different sizes!");
        }

        int j = page * SONGS_IN_PAGE; // Index of the songs in the current page in the database list
        for(int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("EnterButton"))
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "Enter Universe\n" + "[" + 
                    _player.GetComponent<PlayerController>().CurrentClusterId + '.' + clusterId + "]";
                button.onClick.RemoveAllListeners();
                button.onClick.AddListener(() => LaunchButtonEnter(clusterId, isLeaf));
            }

            if(clustButton.CompareTag("SongButton"))
            {
                var button = clustButton.transform.GetChild(0).GetComponent<Button>();
                var background = clustButton.transform.GetChild(0).GetChild(0).gameObject;
                var playButton = clustButton.transform.GetChild(1).gameObject;
                button.onClick.RemoveAllListeners();

                if (j < songsMeta.Count)
                {
                    var songMeta = songsMeta[j];
                    var songTrack = songsTrack[j];
                    background.GetComponentInChildren<Text>().text = songMeta["name"] + " - " + songMeta["artist_name"];
                    button.onClick.AddListener(() => SongClick(songMeta, songTrack));
                    
                    if (playButton.CompareTag("PlayButton"))
                    {
                        playButton.GetComponent<Button>().onClick.RemoveAllListeners();
                        playButton.GetComponent<Button>().onClick.AddListener(() => PlayClick(songMeta));
                    }
                }
                else
                {
                    background.GetComponentInChildren<Text>().text = "";
                }
                j++;
            }

            if(clustButton.CompareTag("ClusterInfoButton"))
            {
                var button = clustButton.GetComponent<Button>();
                button.onClick.RemoveAllListeners();
                button.onClick.AddListener(() => GetClusterInfo(centroid, numSongs));
            }
        }

        GetClusterInfo(centroid, numSongs);
    }

    public void CancelMenu()
    {
        Transform[] children = gameObject.GetComponentsInChildren<Transform>();
        GameObject clustButton;

        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("EnterButton"))
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "Enter Universe\n" + "[]";
                button.onClick.RemoveAllListeners();
            }

            if (clustButton.CompareTag("SongButton"))
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";
                button.onClick.RemoveAllListeners();
            }
        }
    }

    private void SongClick(Dictionary<string, string> meta, Dictionary<string, float> track)
    {
        _featuresLabel.text = "";

        foreach (string key in meta.Keys)
        {
            if(key == "name")
                _featuresLabel.text += "Name : " + meta[key] + "\n"; 
            else if (key == "artist_name")
                _featuresLabel.text += "Artist : " + meta[key] + "\n";
            else if (key == "album_name")
                _featuresLabel.text += "Album : " + meta[key] + "\n";
            else if (key == "playlist")
                _featuresLabel.text += "Playlist : " + meta[key] + "\n";
        }

        _featuresLabel.text += "\n";

        foreach (string key in track.Keys)
        {
            int loopControl = 0;

            if (key != "duration_ms")
            {
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && 
                    key != "time_signature" && key != "popularity")
                {
                    _featuresLabel.text += key + " = " + (track[key] * COORD_MULTIPLIER).ToString("0.00") + "\t\t";
                    for (float i = 0; i < track[key]; i += 1f/10f)
                    {
                        _featuresLabel.text += "♪";
                        loopControl++;
                        if (loopControl > 100)
                            break;
                    }
                }
                else
                {
                    if (key == "popularity")
                    {
                        _featuresLabel.text += key + " = " + track[key].ToString("0") + "\t\t";
                        for (float i = 0; i < track[key]; i += 100f / 10f)
                        {
                            _featuresLabel.text += "♥";
                            loopControl++;
                            if (loopControl > 100)
                                break;
                        }
                    }
                    else if (key == "tempo")
                        _featuresLabel.text += key + " = " + (track[key] * 250).ToString("0") + " BPM";
                    else if(key == "loudness")
                        _featuresLabel.text += key + " = " + track[key].ToString("0.00") + " dB";
                    else if (key == "key" || key == "mode" || key == "time_signature")
                        _featuresLabel.text += key + " = " + track[key];
                }
                
                _featuresLabel.text += "\n";
            }
        }
    }

    private void PlayClick(Dictionary<string, string> meta)
    {
        string uri = "spotify:track:" + meta["id"];
        Application.OpenURL(uri);
    }

    private void LaunchButtonEnter(string clusterId, bool isLeaf)
    {
        _player.GetComponent<PlayerController>().EnterCluster(clusterId, isLeaf);
    }

    private void GetClusterInfo(Dictionary<string, float> centroid, int numSongs)
    {
        _featuresLabel.text = "";
        _featuresLabel.text += "Number of songs" + " : " + numSongs.ToString() + "\n";

        foreach (string key in centroid.Keys)
        {
            int loopControl = 0;

            if (key != "duration_ms")
            {
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && 
                    key != "time_signature" && key != "popularity")
                {
                    _featuresLabel.text += key + " = " + (centroid[key] * COORD_MULTIPLIER).ToString("0.00") + "\t\t";
                    for (float i = 0; i < centroid[key]; i += 1f / 10f)
                    {
                        _featuresLabel.text += "♪";
                        loopControl++;
                        if (loopControl > 100)
                            break;
                    }
                }
                else
                {
                    if (key == "popularity")
                    {
                        _featuresLabel.text += key + " = " + centroid[key] + "\t\t";
                        for (float i = 0; i < centroid[key]; i += 100f / 10f)
                        {
                            _featuresLabel.text += "♥";
                            loopControl++;
                            if (loopControl > 100)
                                break;
                        }
                    }
                    else if (key == "tempo")
                        _featuresLabel.text += key + " = " + (centroid[key] * 250).ToString("0") + " BPM";
                    else if (key == "loudness")
                        _featuresLabel.text += key + " = " + centroid[key].ToString("0.00") + " dB";
                    else if (key == "key" || key == "mode" || key == "time_signature")
                        _featuresLabel.text += key + " = " + centroid[key];
                }

                _featuresLabel.text += "\n";
            }
        }
        string currentClust = _featuresLabel.text;
        _featuresLabel.text += "\n***********  LAST OPENED UNIVERSE:  ***********\n";
        _featuresLabel.text += _prevClust;
        _prevClust = currentClust;
    }
}
