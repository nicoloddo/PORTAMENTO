using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class StatusController : MonoBehaviour
{
    public Text StatusLabel;
    public float clearDelay = 3f; // Time in seconds before clearing
    public bool manualMode = true; // Toggle for manual mode
    
    private Coroutine clearCoroutine;

    // Start is called before the first frame update
    void Start()
    {
        StatusLabel.text = "Give us a sec... We are loading the multiverse!\n" +
            "P.S. Move with WASD, go up/down with Space and Shift, press Esc for the map.";
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void SetStatus(string status)
    {
        StatusLabel.text = status;
        
        if (!manualMode && clearCoroutine != null)
        {
            StopCoroutine(clearCoroutine);
        }
        
        if (!manualMode)
        {
            clearCoroutine = StartCoroutine(ClearStatusAfterDelay());
        }
    }

    private IEnumerator ClearStatusAfterDelay()
    {
        yield return new WaitForSeconds(clearDelay);
        StatusLabel.text = "";
        clearCoroutine = null;
    }
}
