using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class cluster : MonoBehaviour
{
    static int number_of_params_track = 21;    // Numero di parametri numerici
    static int number_of_params_meta = 21;    // Numero di parametri stringa
    private Dictionary<string, float>[] track = new Dictionary<string, float>[number_of_params_track];
    private Dictionary<string, string>[] meta = new Dictionary<string, string>[number_of_params_meta];

    public Dictionary<string, float> centroid = new Dictionary<string, float>();

    public int n_rows = 0;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    public void define_centroid(Dictionary<string, float> centroid_params)
    {
        centroid = centroid_params;
    }

    public void new_cluster_row(Dictionary<string, float> track_line, Dictionary<string, string> meta_line)
    {
        track[n_rows] = new Dictionary<string, float>();
        track[n_rows] = track_line;

        meta[n_rows] = new Dictionary<string, string>();
        meta[n_rows] = meta_line;
    }
}
