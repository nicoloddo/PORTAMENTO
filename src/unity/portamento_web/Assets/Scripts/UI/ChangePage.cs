using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangePage : MonoBehaviour
{
    private GameManager gameManager;

    // Start is called before the first frame update
    void Start()
    {
        gameManager = FindObjectOfType<GameManager>();
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void next_page()
    {
        int page = gameManager.cluster_menu_page + 1;
        gameManager.changepage_songMenu(page);
    }
    public void prev_page()
    {
        int page = gameManager.cluster_menu_page - 1;
        if(page >= 0)
            gameManager.changepage_songMenu(page);
    }
}
