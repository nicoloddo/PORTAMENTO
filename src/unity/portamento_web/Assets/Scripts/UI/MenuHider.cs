using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class MenuHider : MonoBehaviour
{
    [SerializeField] private GameObject[] _menuWindows;  // Drag your window objects here in the Inspector
    public bool IsActive = true;

    public void SetActive(bool active)
    {
        IsActive = active;
        gameObject.GetComponent<Animator>().SetBool("Open", active);

        // Disable/enable TiltWindow components on this object and all children
        TiltWindow[] tiltWindows = gameObject.GetComponentsInChildren<TiltWindow>(true);
        foreach (TiltWindow tiltWindow in tiltWindows)
        {
            tiltWindow.enabled = active;
        }
    }
}
