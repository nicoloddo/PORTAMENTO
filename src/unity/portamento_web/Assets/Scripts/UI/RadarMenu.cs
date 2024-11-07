using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.Linq;

public class RadarMenu : MonoBehaviour
{
    private const int AXIS_MULTIPLIER = 400;  // Also present in the Cluster and DisplayMenu classes
    private const int COORD_MULTIPLIER = 100; // Maximum value of coordinates during display

    private GameObject _player;
    public GameObject Map;
    public GameObject EnterPreviousClusterButton;
    private string _previousClusterId;

    void Start()
    {
        _player = GameObject.FindGameObjectWithTag("Player");
        string currentClusterId = _player.GetComponent<PlayerController>().CurrentClusterId;

        var button = EnterPreviousClusterButton.GetComponent<Button>();
        var background = button.gameObject.transform.GetChild(0).gameObject;

        if (currentClusterId.Length > 1)
        {
            string[] clusterIds = currentClusterId.Split('.');
            _previousClusterId = string.Join(".", clusterIds.Take(clusterIds.Length - 1));

            background.GetComponentInChildren<Text>().text = "Back to Cluster\n" + "[" + 
                _previousClusterId + "]";

            button.onClick.RemoveAllListeners();
            button.onClick.AddListener(() => EnterPreviousCluster());
        }
        else
        {
            background.GetComponentInChildren<Text>().text = "No Cluster to\n go back to yet";
        }
    }

    private void EnterPreviousCluster()
    {
        _player.GetComponent<PlayerController>().EnterCluster(_previousClusterId, false, true);
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
                var button = clustButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                var playButton = button.gameObject.transform.GetChild(1).gameObject;
                button.onClick.RemoveAllListeners();

                if(j < radarMeta.Count)
                {
                    var songMeta = radarMeta[j];
                    var songTrack = radarTrack[j];
                    background.GetComponentInChildren<Text>().text = songMeta["name"] + " - " + songMeta["artist_name"];
                    button.onClick.AddListener(() => SongClick((int)songTrack["label"]));

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
            else if(clustButton.CompareTag("PlayButton"))
            {
                var button = clustButton.GetComponent<Button>();
                button.onClick.RemoveAllListeners();
            }
        }
    }

    public void SongClick(int clusterId)
    {
        Map.GetComponent<MapController>().SelectClusterFromIndex(clusterId);
    }
    public void PlayClick(Dictionary<string, string> meta)
    {
        Application.OpenURL("spotify:track:" + meta["id"]);
    }
}
