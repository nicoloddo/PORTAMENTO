using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongMenu : MonoBehaviour
{
    int axis_multiplier = 400;  // also present in the Cluster and DisplayMenu classes, used to space out clusters
    int coord_multiplier = 100; // maximum value of coordinates during display, used to have a normal scale of judgment instead of a float number or a number with maximum value equal to axis_multiplier
    int songs_in_page = 11; // number of songs in a page

    public GameObject FeaturesContainer;
    private Text featuresLabel;
    private GameObject player;
    private string prev_clust = "";

    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
        featuresLabel = FeaturesContainer.GetComponentInChildren<Text>();
        featuresLabel.text = "Press a song to see its characteristics here.";
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void CreateMenu(bool is_leaf, string cluster_id, List<Dictionary<string, string>> songs_meta, List<Dictionary<string, float>> songs_track, Dictionary<string, float> centroid, int page = 0)
    {
        GameObject clustButton;  // Temporary variable to hold the button
        
        Transform[] children; // Variable to access the children of the menu, i.e., all song_buttons
        children = gameObject.GetComponentsInChildren<Transform>();

        int n_songs = songs_meta.Count;

        if (songs_meta.Count != songs_track.Count)
        {
            Debug.Log("In CreateMenu() songs_meta and songs_track have different sizes!");
        }

        int j = page * songs_in_page;
        for(int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("EnterButton"))
            {   // var button IS NEEDED INSIDE THE IFs BECAUSE NOT ALL CHILDREN OF THE MENU ARE A BUTTON
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "Enter Cluster\n" + "[" + player.GetComponent<PlayerController>().current_cluster_id + cluster_id + "]";
                button.onClick.RemoveAllListeners();
                button.onClick.AddListener(() => launch_button_enter(cluster_id, is_leaf));
            }

            if(clustButton.CompareTag("SongButton"))
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;

                button.onClick.RemoveAllListeners();

                if ( j < songs_meta.Count)
                {
                    var song_m = songs_meta[j];
                    var song_t = songs_track[j];
                    background.GetComponentInChildren<Text>().text = song_m["name"] + " - " + song_m["artist_name"];

                    button.onClick.AddListener(() => song_click(song_m, song_t));
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
                var background = button.gameObject.transform.GetChild(0).gameObject;
                button.onClick.RemoveAllListeners();
                button.onClick.AddListener(() => get_cluster_info(centroid, n_songs));
            }
        }

        get_cluster_info(centroid, n_songs);

    }

    public void CancelMenu()
    {
        Transform[] children; // Variable to access the children of the menu, i.e., all song_buttons
        children = gameObject.GetComponentsInChildren<Transform>();

        GameObject clustButton;

        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("EnterButton"))
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "Enter Cluster\n" + "[]";

                button.onClick.RemoveAllListeners();
            }

            if (clustButton.CompareTag("SongButton")) // Only if it's actually a SongButton
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";

                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void song_click(Dictionary<string, string> meta, Dictionary<string, float> track)
    {
        // FEATURES MENU START
        int loop_control;   // auxiliary var for timely blocking of possible infinite loops

        featuresLabel.text = "";    // Clear the features

        foreach (string key in meta.Keys)
        {
            if(key == "name")
            {
                featuresLabel.text += "Name : " + meta[key] + "\n"; 
            }
            else if (key == "artist_name")
            {
                featuresLabel.text += "Artist : " + meta[key] + "\n";
            }
            else if (key == "album_name")
            {
                featuresLabel.text += "Album : " + meta[key] + "\n";
            }
            else if (key == "playlist")
            {
                featuresLabel.text += "Playlist : " + meta[key] + "\n";
            }
        }

        featuresLabel.text += "\n";

        foreach (string key in track.Keys)
        {
            loop_control = 0;

            if (key != "duration_ms")
            {

                // Put hearts for a visual quantification
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && key != "time_signature" && key != "popularity")
                {
                    featuresLabel.text += key + " = " + (track[key] * coord_multiplier).ToString("0.00") + "\t\t";
                    for (float i = 0; i < track[key]; i += 1f/10f)
                    {
                        featuresLabel.text += "♪";

                        loop_control++;
                        if (loop_control > 100)    // To block the loop in case there's an accidental infinite loop
                            break;
                    }
                }
                else
                {
                    if (key == "popularity")
                    {
                        featuresLabel.text += key + " = " + track[key].ToString("0") + "\t\t";
                        for (float i = 0; i < track[key]; i += 100f / 10f)  // Popularity goes from 0 to 100
                        {
                            featuresLabel.text += "♥";

                            loop_control++;
                            if (loop_control > 100)    // To block the loop in case there's an accidental infinite loop
                                break;
                        }
                    }
                    else if (key == "tempo")
                    {
                        featuresLabel.text += key + " = " + (track[key] * 250).ToString("0") + " BPM";   // Denormalize the tempo. For display it's better to express it in BPM
                    }
                    else if(key == "loudness")
                    {
                        featuresLabel.text += key + " = " + track[key].ToString("0.00") + " dB";
                    }
                    else if (key == "key" || key == "mode" || key == "time_signature")
                    {
                        featuresLabel.text += key + " = " + track[key];
                    }
                }
                
                featuresLabel.text += "\n";
            }
        }

        string uri = "spotify:track:" + meta["id"];
        Application.OpenURL(uri);
    }

    public void launch_button_enter(string cluster_id, bool is_leaf)
    {
        player.GetComponent<PlayerController>().enterCluster(cluster_id, is_leaf);
    }

    public void get_cluster_info(Dictionary<string, float> centroid, int n_songs)
    {
        int loop_control;   // auxiliary var for timely blocking of possible infinite loops

        featuresLabel.text = "";    // Clear the features

        featuresLabel.text += "Number of songs" + " : " + n_songs.ToString() + "\n";

        foreach (string key in centroid.Keys)
        {
            loop_control = 0;

            if (key != "duration_ms")
            {

                // Put hearts for a visual quantification
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && key != "time_signature" && key != "popularity")
                {
                    featuresLabel.text += key + " = " + (centroid[key] * coord_multiplier).ToString("0.00") + "\t\t";
                    for (float i = 0; i < centroid[key]; i += 1f / 10f)
                    {
                        featuresLabel.text += "♪";

                        loop_control++;
                        if (loop_control > 100)    // To block the loop in case there's an accidental infinite loop
                            break;
                    }
                }
                else
                {
                    if (key == "popularity")
                    {
                        featuresLabel.text += key + " = " + centroid[key] + "\t\t";
                        for (float i = 0; i < centroid[key]; i += 100f / 10f)  // Popularity goes from 0 to 100
                        {
                            featuresLabel.text += "♥";

                            loop_control++;
                            if (loop_control > 100)    // To block the loop in case there's an accidental infinite loop
                                break;
                        }
                    }
                    else if (key == "tempo")
                    {
                        featuresLabel.text += key + " = " + (centroid[key] * 250).ToString("0") + " BPM";   // Value through which I had normalized the tempo. For display it's better to express it in BPM
                    }
                    else if (key == "loudness")
                    {
                        featuresLabel.text += key + " = " + centroid[key].ToString("0.00") + " dB";
                    }
                    else if (key == "key" || key == "mode" || key == "time_signature")
                    {
                        featuresLabel.text += key + " = " + centroid[key];
                    }
                }

                featuresLabel.text += "\n";
            }
        }
        string current_clust = featuresLabel.text;
        featuresLabel.text += "\n***********  LAST OPENED CLUSTER:  ***********\n";
        featuresLabel.text += prev_clust;
        prev_clust = current_clust;
    }
}
