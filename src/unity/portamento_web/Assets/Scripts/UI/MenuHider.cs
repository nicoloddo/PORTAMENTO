using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class MenuHider : MonoBehaviour
{
    [SerializeField] private GameObject[] _menuWindows;  // Drag your window objects here in the Inspector
    private bool _isActive = true;

    public bool IsActive
    {
        get { return _isActive; }
    }

    public void SetActive(bool active)
    {
        _isActive = active;
        gameObject.GetComponent<Animator>().SetBool("Open", active);
    }
}
