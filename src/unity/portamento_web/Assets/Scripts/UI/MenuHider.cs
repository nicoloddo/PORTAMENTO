using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.EventSystems;

public class MenuHider : MonoBehaviour
{
    [SerializeField] private GameObject[] _menuWindows;  // Drag your window objects here in the Inspector
    [SerializeField] private MenuHider[] _showWhenHidden;  // New array for objects to show when menu is hidden
    [SerializeField] private MenuHider[] _hideWhenHidden;  // New array for objects to hide when menu is hidden
    public bool IsActive = false;

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

        // Set inverse active state for objects that should show when menu is hidden
        if (_showWhenHidden != null && !active)
        {
            foreach (MenuHider obj in _showWhenHidden)
            {
                if (obj != null)
                    obj.SetActive(true);
            }
        }

        // Set active state for objects that should hide when menu is hidden
        if (_hideWhenHidden != null && !active)
        {
            foreach (MenuHider obj in _hideWhenHidden)
            {
                if (obj != null)
                    obj.SetActive(false);
            }
        }
    }
}
