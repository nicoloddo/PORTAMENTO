using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangePage : MonoBehaviour
{
    private GameManager _gameManager;

    void Start()
    {
        _gameManager = FindAnyObjectByType<GameManager>();
    }

    public void NextPage()
    {
        int page = _gameManager.ClusterMenuPage + 1;
        _gameManager.ChangePageSongMenu(page);
    }

    public void PrevPage()
    {
        int page = _gameManager.ClusterMenuPage - 1;
        if(page >= 0)
            _gameManager.ChangePageSongMenu(page);
    }
}
