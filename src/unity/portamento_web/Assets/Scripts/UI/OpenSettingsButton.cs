using UnityEngine;

public class OpenSettingsButton : MonoBehaviour
{
    public GameObject SettingsMenu;
    [SerializeField] private MenuHider[] _hideWhenOpening;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void OpenSettings()
    {
        SettingsMenu.GetComponent<MenuHider>().SetActive(true);
        
        foreach (MenuHider obj in _hideWhenOpening)
        {
            if (obj != null)
                obj.SetActive(false);
        }
    }
}
