using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class get_clusters : MonoBehaviour
{
    private static string PATHS_FILE_NAME = @"\last_path.csv";

    private string current_path = System.IO.Directory.GetCurrentDirectory();
    public string base_path;

    Dictionary<string, string> paths = new Dictionary<string, string>();

    // Start is called before the first frame update
    void Start()
    {
        base_path = current_path.Remove(current_path.Length - 27);  // 27 PERCHE' QUESTO E' IL NUMERO DI CARATTERI DA CANCELLARE PER OTTENERE IL base_path
        string last_path_file = string.Concat(base_path, PATHS_FILE_NAME);

        paths = strings_csv_to_dict(last_path_file);
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }

    private Dictionary<string, string> strings_csv_to_dict(string path_csv)
    {
        Dictionary<string, string> dict = new Dictionary<string, string>();
        string file_data = System.IO.File.ReadAllText(path_csv);
        string[] keys = file_data.Split('\n')[0].Split(',');
        

        return dict;
    }
}
