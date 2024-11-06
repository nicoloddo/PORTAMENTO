using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeAxisButton : MonoBehaviour
{
    public GameObject Map;
    
    public void NextAxisX()
    {
        Map.GetComponent<MapController>().IncrementX(1);
    }

    public void NextAxisY()
    {
        Map.GetComponent<MapController>().IncrementY(1);
    }

    public void PrevAxisX()
    {
        Map.GetComponent<MapController>().IncrementX(-1);
    }

    public void PrevAxisY()
    {
        Map.GetComponent<MapController>().IncrementY(-1);
    }
}
