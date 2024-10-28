using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RadarMenu : MonoBehaviour
{
    int axis_multiplier = 400;  // Also present in the Cluster and DisplayMenu classes, used to space out clusters
    int coord_multiplier = 100; // Maximum value of coordinates during display, used to have a normal scale of judgment instead of a float number or a number with maximum value equal to axis_multiplier

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
        GameObject clustButton;  // Temporary variable to hold the button

        Transform[] children; // Variable to access the children of the menu, i.e., all song_buttons
        children = gameObject.GetComponentsInChildren<Transform>();

        if (radar_meta.Count != radar_track.Count)
        {
            Debug.Log("In CreateMenu() songs_meta and songs_track have different numbers of songs!");
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

                    button.onClick.AddListener(() => song_click((int) song_t["label"], song_m["uri"]));

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
        Transform[] children; // Variable to access the children of the menu, i.e., all song_buttons
        children = gameObject.GetComponentsInChildren<Transform>();

        GameObject clustButton;

        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("SongButton")) // Only if it's actually a SongButton
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";

                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void song_click(int cluster_id, string url)
    {
        map.GetComponent<MapController>().select_cluster_from_index(cluster_id);

        Application.OpenURL(url);
    }
}
