using UnityEngine;

public class SettingsController : MonoBehaviour
{
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

    public void ResetSettings()
    {
        PlayerPrefs.DeleteAll();
        Animator animator = GetComponent<Animator>();
        //animator.SetBool("Pressed", false);
        //animator.Play("Normal");
        GameManager gameManager = FindAnyObjectByType<GameManager>();
        gameManager.StatusLabel.SetStatus("The settings have been reset");
    }

    public void SetSpotifyInstalledYes()
    {
        PlayerPrefs.SetInt("spotifyInstalled", 1);
    }

    public void SetSpotifyInstalledNo()
    {
        PlayerPrefs.SetInt("spotifyInstalled", 0);
    }
}
