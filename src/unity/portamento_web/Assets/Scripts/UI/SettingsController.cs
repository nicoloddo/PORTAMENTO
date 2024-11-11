using UnityEngine;
using UnityEngine.UI;

public class SettingsController : MonoBehaviour
{
    public GameObject OppositeButton;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void CloseSettings()
    {
        GetComponentInParent<MenuHider>().SetActive(false);
    }

    public void SetSpotifyInstalledYes()
    {
        PlayerPrefs.SetInt("spotifyInstalled", 1);
        GetComponentInChildren<Image>().color = new Color(1, 1, 1, 1);
        GameObject oppositeBackground = OppositeButton.transform.GetChild(0).gameObject;
        oppositeBackground.GetComponent<Image>().color = new Color(0, 140f/255f, 1, 1);

    }

    public void SetSpotifyInstalledNo()
    {
        PlayerPrefs.SetInt("spotifyInstalled", 0);
        GetComponentInChildren<Image>().color = new Color(1, 1, 1, 1);
        GameObject oppositeBackground = OppositeButton.transform.GetChild(0).gameObject;
        oppositeBackground.GetComponent<Image>().color = new Color(0, 140f/255f, 1, 1);
    }
}
