using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RadarMenu : MonoBehaviour
{
    int axis_multiplier = 400;  // presente anche nella classe Cluster e DisplayMenu serve a distanziare i cluster
    int coord_multiplier = 100; // valore massimo delle coordinate durante il display, serve ad avere un metro di giudizio normale anzichè avere un numero float o un numero con valore massimo pari all'axis_multiplier

    private GameObject player;
    public GameObject map;

    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
    }

    // Update is called once per frame
    void Update()
    {

    }

    public void CreateMenu(List<Dictionary<string, string>> radar_meta, List<Dictionary<string, float>> radar_track)
    {
        GameObject clustButton;  // Variabile temporanea in cui metto il button

        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
        children = gameObject.GetComponentsInChildren<Transform>();

        if (radar_meta.Count != radar_track.Count)
        {
            Debug.Log("In CreateMenu() songs_meta e songs_track hanno un numero di canzoni diversi!");
        }

        int j = 0;
        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("SongButton"))
            {
                if(j < radar_meta.Count)
                {
                    var song_m = radar_meta[j];
                    var song_t = radar_track[j];
                    var button = clustButton.GetComponent<Button>();
                    var background = button.gameObject.transform.GetChild(0).gameObject;
                    background.GetComponentInChildren<Text>().text = song_m["name"] + " - " + song_m["artist"];

                    button.onClick.AddListener(() => launch_button_song((int) song_t["label"], song_m["uri"]));

                    j++;
                }
                else
                {
                    var button = clustButton.GetComponent<Button>();
                    var background = button.gameObject.transform.GetChild(0).gameObject;
                    background.GetComponentInChildren<Text>().text = "";
                }
                
            }
        }

    }

    public void CancelMenu()
    {
        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
        children = gameObject.GetComponentsInChildren<Transform>();

        GameObject clustButton;

        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("SongButton")) // Solo se è effettivamente un SongButton
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";

                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void launch_button_song(int cluster_id, string url)
    {
        map.GetComponent<MapController>().launch_button_from_index(cluster_id);

        Application.OpenURL(url);
    }
}
