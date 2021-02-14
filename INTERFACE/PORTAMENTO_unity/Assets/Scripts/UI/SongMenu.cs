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

    public void CreateMenu(List<Dictionary<string, string>> songs_meta)
    {
        GameObject songButton;  // Variabile temporanea in cui metto il song_button per ogni canzone
        int i = 0;
        foreach(var song in songs_meta)
        {
            try
            {
                do
                {
                    songButton = gameObject.transform.GetChild(i).gameObject;
                    i += 1;
                } while (!songButton.CompareTag("SongButton"));

                var button = songButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = song["name"] + " - " + song["artist"];

                string url = song["uri"];
                button.onClick.AddListener(() => launch_song(url));
            }
            catch (UnityException)   // Ci sarà una eccezione appena finiscono gli oggetti child
            {
            }
        }
        
    }

    public void launch_song(string url)
    {
        Application.OpenURL(url);
    }
}
