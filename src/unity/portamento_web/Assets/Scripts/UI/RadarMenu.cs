using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class RadarMenu : MonoBehaviour
{
    private const int AXIS_MULTIPLIER = 400;  // Also present in the Cluster and DisplayMenu classes
    private const int COORD_MULTIPLIER = 100; // Maximum value of coordinates during display

    private GameObject _player;
    public GameObject Map;

    void Start()
    {
        _player = GameObject.FindGameObjectWithTag("Player");
    }

    public void CreateMenu(List<Dictionary<string, string>> radarMeta, List<Dictionary<string, float>> radarTrack)
    {
        GameObject clustButton;  // Temporary variable to hold the button

        Transform[] children = gameObject.GetComponentsInChildren<Transform>();

        if (radarMeta.Count != radarTrack.Count)
        {
            Debug.Log("In CreateMenu() songs_meta and songs_track have different numbers of songs!");
        }

        int j = 0;
        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("SongButton"))
            {
                if(j < radarMeta.Count)
                {
                    var songMeta = radarMeta[j];
                    var songUri = "spotify:track:" + songMeta["id"];
                    var songTrack = radarTrack[j];
                    var button = clustButton.GetComponent<Button>();
                    var background = button.gameObject.transform.GetChild(0).gameObject;
                    background.GetComponentInChildren<Text>().text = songMeta["name"] + " - " + songMeta["artist_name"];

                    button.onClick.AddListener(() => SongClick((int)songTrack["label"], songUri));

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
        Transform[] children = gameObject.GetComponentsInChildren<Transform>();
        GameObject clustButton;

        for (int i = 0; i < children.Length; i++)
        {
            clustButton = children[i].gameObject;

            if (clustButton.CompareTag("SongButton"))
            {
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = "";
                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void SongClick(int clusterId, string url)
    {
        Map.GetComponent<MapController>().SelectClusterFromIndex(clusterId);
        Application.OpenURL(url);
    }
}
