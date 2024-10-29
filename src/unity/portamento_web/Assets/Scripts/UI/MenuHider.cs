using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class MenuHider : MonoBehaviour
{
    [SerializeField] private GameObject[] menuWindows;  // Drag your window objects here in the Inspector
    private bool isActive = true;

    public void SetActive(bool active)
    {
        isActive = active;
        gameObject.GetComponent<Animator>().SetBool("Open", active);
    }

    public bool IsActive()
    {
        return isActive;
    }
}
