using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongMenu : MonoBehaviour
{
    int axis_multiplier = 400;  // presente anche nella classe Cluster e DisplayMenu serve a distanziare i cluster
    int coord_multiplier = 100; // valore massimo delle coordinate durante il display, serve ad avere un metro di giudizio normale anzichè avere un numero float o un numero con valore massimo pari all'axis_multiplier
    int songs_in_page = 11; // numero di canzoni in una pagina

    public GameObject FeaturesContainer;
    private Text featuresLabel;
    private GameObject player;
    private string prev_clust = "";

    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
        featuresLabel = FeaturesContainer.GetComponentInChildren<Text>();
        featuresLabel.text = "Premi una canzone per vedere le sue caratteristiche qui.";
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void CreateMenu(bool is_leaf, string cluster_id, List<Dictionary<string, string>> songs_meta, List<Dictionary<string, float>> songs_track, Dictionary<string, float> centroid, int page = 0)
    {
        GameObject clustButton;  // Variabile temporanea in cui metto il button
        
        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
        children = gameObject.GetComponentsInChildren<Transform>();

        int n_songs = songs_meta.Count;

        if (songs_meta.Count != songs_track.Count)
        {
            Debug.Log("In CreateMenu() songs_meta e songs_track sono di grandezze diverse!");
        }

        int j = page * songs_in_page;
        for(int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("EnterButton"))
            {   // var button SERVE DENTRO AGLI IF PERCHE' NON TUTTI I FIGLI DEL MENù HANNO UN BOTTONE
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
                    background.GetComponentInChildren<Text>().text = song_m["name"] + " - " + song_m["artist"];

                    button.onClick.AddListener(() => launch_button_song(song_m, song_t));
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
                button.onClick.AddListener(() => launch_button_cluster_info(centroid, n_songs));
            }
        }

        launch_button_cluster_info(centroid, n_songs);

    }

    public void CancelMenu()
    {
        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
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

            if (clustButton.CompareTag("SongButton")) // Solo se è effettivamente un SongButton
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";

                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void launch_button_song(Dictionary<string, string> meta, Dictionary<string, float> track)
    {
        // FEATURES MENU AVVIO
        int loop_control;   // var ausiliaria per il blocco tempestivo di possibili loop infiniti

        featuresLabel.text = "";    // Cancello le features

        foreach (string key in meta.Keys)
        {
            if(key == "name" || key == "artist" || key == "album" || key == "playlist")
            {
                featuresLabel.text += key + " : " + meta[key] + "\n"; 
            }
        }

        featuresLabel.text += "\n";

        foreach (string key in track.Keys)
        {
            loop_control = 0;

            if (key != "duration_ms")
            {

                // Metto cuori per una quantificazione visuale
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && key != "time_signature" && key != "popularity")
                {
                    featuresLabel.text += key + " = " + (track[key] * coord_multiplier).ToString("0.00") + "\t\t";
                    for (float i = 0; i < track[key]; i += 1f/10f)
                    {
                        featuresLabel.text += "♪";

                        loop_control++;
                        if (loop_control > 100)    // Per bloccare il loop nel caso in cui ci sia per sbaglio un loop infinito
                            break;
                    }
                }
                else
                {
                    if (key == "popularity")
                    {
                        featuresLabel.text += key + " = " + track[key].ToString("0") + "\t\t";
                        for (float i = 0; i < track[key]; i += 100f / 10f)  // La popolarità va da 0 a 100
                        {
                            featuresLabel.text += "♥";

                            loop_control++;
                            if (loop_control > 100)    // Per bloccare il loop nel caso in cui ci sia per sbaglio un loop infinito
                                break;
                        }
                    }
                    else if (key == "tempo")
                    {
                        featuresLabel.text += key + " = " + (track[key] * 250).ToString("0") + " BPM";   // Denormalizzo il tempo. Per il display è meglio esprimerlo in BPM
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

        string url = meta["uri"];
        Application.OpenURL(url);
    }

    public void launch_button_enter(string cluster_id, bool is_leaf)
    {
        player.GetComponent<PlayerController>().enterCluster(cluster_id, is_leaf);
    }

    public void launch_button_cluster_info(Dictionary<string, float> centroid, int n_songs)
    {
        int loop_control;   // var ausiliaria per il blocco tempestivo di possibili loop infiniti

        featuresLabel.text = "";    // Cancello le features

        featuresLabel.text += "Numero di canzoni" + " : " + n_songs.ToString() + "\n";

        foreach (string key in centroid.Keys)
        {
            loop_control = 0;

            if (key != "duration_ms")
            {

                // Metto cuori per una quantificazione visuale
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && key != "time_signature" && key != "popularity")
                {
                    featuresLabel.text += key + " = " + (centroid[key] * coord_multiplier).ToString("0.00") + "\t\t";
                    for (float i = 0; i < centroid[key]; i += 1f / 10f)
                    {
                        featuresLabel.text += "♪";

                        loop_control++;
                        if (loop_control > 100)    // Per bloccare il loop nel caso in cui ci sia per sbaglio un loop infinito
                            break;
                    }
                }
                else
                {
                    if (key == "popularity")
                    {
                        featuresLabel.text += key + " = " + centroid[key] + "\t\t";
                        for (float i = 0; i < centroid[key]; i += 100f / 10f)  // La popolarità va da 0 a 100
                        {
                            featuresLabel.text += "♥";

                            loop_control++;
                            if (loop_control > 100)    // Per bloccare il loop nel caso in cui ci sia per sbaglio un loop infinito
                                break;
                        }
                    }
                    else if (key == "tempo")
                    {
                        featuresLabel.text += key + " = " + (centroid[key] * 250).ToString("0") + " BPM";   // Valore tramite il quale avevo normalizzato il tempo. Per il display è meglio esprimerlo in BPM
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
        featuresLabel.text += "\n***********  ULTIMO CLUSTER APERTO:  ***********\n";
        featuresLabel.text += prev_clust;
        prev_clust = current_clust;
    }
}
