using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class get_clusters : MonoBehaviour
{
    private static string PATHS_FILE_NAME = "last_path.csv";

    private string current_path = System.IO.Directory.GetCurrentDirectory();
    public string base_path;

    Dictionary<string, string> paths = new Dictionary<string, string>();

    // Start is called before the first frame update
    void Start()
    {
        base_path = current_path.Remove(current_path.Length - 52);
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private Dictionary<string, string> string_keys_csv_to_dict(string path_csv)
    {
        Dictionary<string, string> dict = new Dictionary<string, string>();
        string Data = System.IO.File.ReadAllText(path_csv);

        return dict;
    }
}
