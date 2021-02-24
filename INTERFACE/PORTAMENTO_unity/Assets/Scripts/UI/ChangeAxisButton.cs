using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ChangeAxisButton : MonoBehaviour
{
    public GameObject map;
    
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void next_axis_x()
    {
        map.GetComponent<MapController>().increment_x(1);
    }
    public void next_axis_y()
    {
        map.GetComponent<MapController>().increment_y(1);
    }
    public void prev_axis_x()
    {
        map.GetComponent<MapController>().increment_x(-1);
    }
    public void prev_axis_y()
    {
        map.GetComponent<MapController>().increment_y(-1);
    }
}
