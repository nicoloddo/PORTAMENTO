using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class DisplayMenu : MonoBehaviour
{
    int axis_multiplier = 400;  // presente anche nella classe Cluster serve a distanziare i cluster
    int coord_multiplier = 100; // valore massimo delle coordinate durante il display, serve ad avere un metro di giudizio normale anzichè avere un numero float o un numero con valore massimo pari all'axis_multiplier

    private GameObject player;
    private Vector3 player_pos;
    private string[] axis_labels = new string[3];
    private string[] pos = new string[3];

    public Text coordsLabel;
    public Text clusterLabel;


    // Start is called before the first frame update
    void Start()
    {
        player = GameObject.FindGameObjectWithTag("Player");
    }

    // Update is called once per frame
    void Update()
    {
        player_pos = player.transform.position;
        for (int i = 0; i < 3; i++)
        {
            if(axis_labels[i] != "tempo")
            {
                pos[i] = (player_pos[i]/axis_multiplier*coord_multiplier).ToString("0.00"); // Divide by axis_multiplier to normalize it, then multiply by coord_multiplier
            }
            else
            {
                pos[i] = (player_pos[i]/axis_multiplier*250).ToString("0.00");
            }
        }
            
        coordsLabel.text = axis_labels[0] + " = " + pos[0] + "\n" +
                           axis_labels[2] + " = " + pos[2] + "\n" +
                           axis_labels[1] + " = " + pos[1];
        clusterLabel.text = "Cluster ID: " + player.GetComponent<PlayerController>().current_cluster_id;
    }

    public void set_axis_labels(string axis1, string axis2, string axis3)
    {
        axis_labels[0] = axis1;
        axis_labels[1] = axis2;
        axis_labels[2] = axis3;
    }
}
