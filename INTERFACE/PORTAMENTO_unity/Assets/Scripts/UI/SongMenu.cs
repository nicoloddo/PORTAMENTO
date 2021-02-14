using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SongMenu : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    void CreateMenu(List<Dictionary<string, string>> songs_meta)
    {
        int i = 0;
        foreach(var song in songs_meta)
        {
            var songButton = gameObject.transform.GetChild(i).gameObject;
            var button = songButton.GetComponent<Button>();
            var background = button.gameObject.transform.GetChild(0).gameObject;
            background.GetComponentInChildren<Text>().text = song["name"] + " - " + song["artist"];
            button.onClick.AddListener(() => launch_song(song["url"]));
        }
        
    }

    public void launch_song(string url)
    {
        Application.OpenURL(url);
    }
}
