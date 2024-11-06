using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisplayMenu : MonoBehaviour
{
    private const int AXIS_MULTIPLIER = 400;  // Also present in Cluster class, used to space out clusters
    private const int COORD_MULTIPLIER = 100; // Maximum value of coordinates during display, used to have a normal scale

    private GameObject _player;
    private Vector3 _playerPos;
    private string[] _axisLabels = new string[3];
    private string[] _pos = new string[3];

    public Text CoordsLabel;
    public Text ClusterLabel;

    void Start()
    {
        _player = GameObject.FindGameObjectWithTag("Player");
    }

    void Update()
    {
        _playerPos = _player.transform.position;
        for (int i = 0; i < 3; i++)
        {
            if(_axisLabels[i] != "tempo")
            {
                _pos[i] = (_playerPos[i]/AXIS_MULTIPLIER*COORD_MULTIPLIER).ToString("0.00"); // Normalize and scale for display
            }
            else
            {
                _pos[i] = (_playerPos[i]/AXIS_MULTIPLIER*250).ToString("0.00");
            }
        }
            
        CoordsLabel.text = _axisLabels[0] + " = " + _pos[0] + "\n" +
                          _axisLabels[2] + " = " + _pos[2] + "\n" +
                          _axisLabels[1] + " = " + _pos[1];
        ClusterLabel.text = "Cluster ID: " + _player.GetComponent<PlayerController>().CurrentClusterId;
    }

    public void SetAxisLabels(string axis1, string axis2, string axis3)
    {
        _axisLabels[0] = axis1;
        _axisLabels[1] = axis2;
        _axisLabels[2] = axis3;
    }
}
