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
        
        Transform[] children; // Variabile da cui accedo ai figli del menu, ossia tutti i song_button
        children = gameObject.GetComponentsInChildren<Transform>();

        int j = 0;
        for(int i = 0; i < songs_meta.Count; i++)
        {
            var song = songs_meta[i];

            try
            {
                do
                {
                    songButton = children[j].gameObject;
                    j += 1;
                } while (!songButton.CompareTag("SongButton") && j < children.Length);

                var button = songButton.GetComponent<Button>();
                var background = button.gameObject.transform.GetChild(0).gameObject;
                background.GetComponentInChildren<Text>().text = song["name"] + " - " + song["artist"];

                string url = song["uri"];
                button.onClick.AddListener(() => launch_song(url));
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

    public void launch_song(string url)
    {
        Application.OpenURL(url);
    }
}
