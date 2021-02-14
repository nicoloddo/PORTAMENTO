using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongMenu : MonoBehaviour
{
    public GameObject FeaturesContainer;
    private Text featuresLabel;

    // Start is called before the first frame update
    void Start()
    {
        featuresLabel = FeaturesContainer.GetComponentInChildren<Text>();
        featuresLabel.text = "Premi una canzone per vedere le sue caratteristiche qui.";
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void CreateMenu(List<Dictionary<string, string>> songs_meta, List<Dictionary<string, float>> songs_track)
    {
        GameObject songButton;  // Variabile temporanea in cui metto il song_button per ogni canzone
        
        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
        children = gameObject.GetComponentsInChildren<Transform>();

        if(songs_meta.Count != songs_track.Count)
        {
            Debug.Log("In CreateMenu() songs_meta e songs_track sono di grandezze diverse!");
        }

        int j = 0;
        for(int i = 0; i < songs_meta.Count; i++)
        {
            var song_m = songs_meta[i];
            var song_t = songs_track[i];

            try
            {
                do
                {
                    songButton = children[j].gameObject;
                    j += 1;
                } while (!songButton.CompareTag("SongButton") && j < children.Length);

                if(songButton.CompareTag("SongButton"))
                {
                    var button = songButton.GetComponent<Button>();
                    var background = button.gameObject.transform.GetChild(0).gameObject;
                    background.GetComponentInChildren<Text>().text = song_m["name"] + " - " + song_m["artist"];

                    button.onClick.AddListener(() => launch_button_song(song_m, song_t));
                }    
            }
            catch (System.IndexOutOfRangeException)   // Ci sarà una eccezione appena finiscono gli oggetti child
            {
            }

            if (j == children.Length)   // Abbiamo finito i tasti, dovremmo 
                break;
        }
        
    }

    public void CancelMenu()
    {
        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
        children = gameObject.GetComponentsInChildren<Transform>();

        GameObject songButton;

        for (int i = 0; i < children.Length; i++)
        {
            songButton = children[i].gameObject;

            if (songButton.CompareTag("SongButton")) // Solo se è effettivamente un SongButton
            {
                var button = songButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";

                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void launch_button_song(Dictionary<string, string> meta, Dictionary<string, float> track)
    {
        int loop_control;   // var ausiliaria per il blocco tempestivo di possibili loop infiniti

        featuresLabel.text = "";    // Cancello le features

        foreach (string key in meta.Keys)
        {
            if(key == "name" || key == "artist" || key == "album")
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
                if(key != "tempo")
                    featuresLabel.text += key + " = " + track[key] + " ";
                else if(key == "tempo")
                    featuresLabel.text += key + " = " + track[key]*250 + " ";   // Valore tramite il quale avevo normalizzato il tempo. Per il display è meglio esprimerlo in BPM

                // Metto cuori per una quantificazione visuale
                if (key != "key" && key != "loudness" && key != "mode" && key != "tempo" && key != "time_signature" && key != "popularity")
                {
                    featuresLabel.text += "\t\t";
                    for (float i = 0; i < track[key]; i += 1f / 10f)
                    {
                        featuresLabel.text += "♪";

                        loop_control++;
                        if (loop_control > 100)    // Per bloccare il loop nel caso in cui ci sia per sbaglio un loop infinito
                            break;
                    }
                }
                if(key == "popularity")
                {
                    featuresLabel.text += "\t\t";
                    for (float i = 0; i < track[key]; i += 100f / 10f)
                    {
                        featuresLabel.text += "♥";

                        loop_control++;
                        if (loop_control > 100)    // Per bloccare il loop nel caso in cui ci sia per sbaglio un loop infinito
                            break;
                    }
                }   
                if (key == "tempo")
                    featuresLabel.text += " BPM";

                featuresLabel.text += "\n";
            }
        }

        string url = meta["uri"];
        Application.OpenURL(url);
    }
}
