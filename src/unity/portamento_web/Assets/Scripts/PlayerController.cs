using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    int axis_multiplier = 400; // Presente anche nella classe SongMenu, DisplayMenu e Cluster: serve a distanziare i cluster

    // ASSEGNAZIONI UTILI
    private Animator animator;
    private CharacterController characterController;
    public Vector3 lookat_rotation;

    // JUST PRESSED
    float just_pressed = 0; // Serve ad aspettare prima di ricevere un nuovo input. Per evitare che si richiuda subito un menù se premiamo leggermente troppo
    float just_pressed_max = 0.1f;

    // LINKS
    public GameObject camera;
    private GameManager gameManager;
    private GameObject nearCluster;

    // BOOLS
    private bool starting = true;
    private bool first_run = true;
    public bool is_near = false;
    public bool can_move = true;
    private bool song_menu_opened = false;
    private bool map_opened = false;

    // INPUTS
    private float inputUpward; // Per muoversi verso sù
    private float inputVertical; //Tasti per muoversi in avanti
    private float inputHorizontal; //Tasti per ruotare (oltre al mouse)
    public float totalXRot; //Rotazione in X totale
    public float totalYRot; //Rotazione in Y totale

    // PARAMETRI
    private float rotateSpeedX = 4f; //Velocita' di rotazione X
    private float rotateSpeedY = 3f; //Velocita' di rotazione Y
    public float forwardSpeed = 0.8f; // Velocità di avanzamento
    public float lateralSpeed = 0.5f; // Velocità movimento laterale
    public float upwardSpeed = 0.5f; // Velocità di levitazione

    // NAVIGAZIONE
    public string current_cluster_id = "0";
    public Transform selected_clust_transform;

    private void Awake()
    {
        gameManager = FindObjectOfType<GameManager>();
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();

        if (PlayerPrefs.HasKey("current_cluster_id"))
        {
            current_cluster_id = PlayerPrefs.GetString("current_cluster_id");
            starting = false;
        }
        else
        {
            current_cluster_id = "0";
        }
    }

    void Start()
    {
        // DEVO RICORDARMI, PRIMA DI AVVIARE IL "VIAGGIO" DI UTILIZZARE LO SCRIPT start_trip.py
        enterCluster(current_cluster_id, false, starting, true);   // All'inizio del caricamento della scena eseguiamo il ClustersInterface
    }

    // Update is called once per frame
    void Update()
    {
        if(just_pressed < just_pressed_max + 5)
        just_pressed += Time.deltaTime;

        if (first_run)
        {
            // disattivo e riattivo il character controller perchè non mi permette il teletrasporto
            gameObject.GetComponent<CharacterController>().enabled = false;
            transform.position = get_start();
            first_run = false;
            gameObject.GetComponent<CharacterController>().enabled = true;
        }

        if (Input.GetKey("f") && is_near && !map_opened && just_pressed > just_pressed_max)
        {
            if(!song_menu_opened)
            {
                song_menu_run();
                animator.SetFloat("fly", 0);    // Lo faccio fermare
                just_pressed = 0;   // avvio il timer
            }
            else if(just_pressed > 1)
            {
                song_menu_esc();
                just_pressed = 0;   // avvio il timer
            }  
        }

        if (Input.GetKey("m") && !song_menu_opened && just_pressed > just_pressed_max)
        {
            if (!map_opened)
            {
                map_show();
                animator.SetFloat("fly", 0);    // Lo faccio fermare
                just_pressed = 0;   // avvio il timer
            }
            else if (just_pressed > 1)
            {
                map_esc();
                just_pressed = 0;   // avvio il timer
            }
        }

        if (Input.GetKey("r") && !song_menu_opened && !map_opened)
        {
            transform.LookAt(selected_clust_transform);
            totalXRot = transform.rotation.eulerAngles.y;
            totalYRot = transform.rotation.eulerAngles.x;
        }

        if (Input.GetKey("z") && !song_menu_opened && !map_opened)
        {
            totalYRot = 0;
        }

        if (Input.GetKey("x") && !song_menu_opened && !map_opened)
        {
            if (!Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = 90;
                totalYRot = 0;
            }
            if (Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = -90;
                totalYRot = 0;
            }
        }

        if (Input.GetKey("c") && !song_menu_opened && !map_opened)
        {
            if (!Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = 0;
                totalYRot = 0;
            }
            if (Input.GetKey(KeyCode.LeftControl))
            {
                totalXRot = 180;
                totalYRot = 0;
            }
        }
    }


    private void FixedUpdate()
    {
        // ******************* GESTIONE DEL MOVIMENTO
        if (can_move)
        {
            inputVertical = Input.GetAxis("Vertical");
            inputHorizontal = Input.GetAxis("Horizontal");
            inputUpward = Input.GetAxis("Jump");

            animator.SetFloat("fly", inputVertical);

            // Controller della rotazione, è fatto così per evitare la rotazione in z, che può avvenire per somma di rotazioni in x e y
            totalXRot += Input.GetAxis("Mouse X") * rotateSpeedX;
            totalYRot -= Input.GetAxis("Mouse Y") * rotateSpeedY;

            transform.forward = camera.transform.forward;

            if (inputVertical > 0)
            {
                camera.transform.rotation = Quaternion.Euler(totalYRot, totalXRot, 0f);
            }
            else
            {
                camera.transform.rotation = transform.rotation;
                transform.rotation = Quaternion.Euler(0f, totalXRot, 0f);
                camera.transform.rotation = Quaternion.Euler(totalYRot, totalXRot, 0f);
            }

            // Movimento
            characterController.Move(camera.transform.forward * inputVertical * forwardSpeed);
            characterController.Move(camera.transform.right * inputHorizontal * forwardSpeed);
            characterController.Move(camera.transform.up * inputUpward * upwardSpeed);

            // ******************* FINE GESTIONE MOVIMENTO
        }
    }

    private void map_show()
    {
        map_opened = true;

        can_move = false;

        gameManager.view_map();
    }

    private void map_esc()
    {
        map_opened = false;

        can_move = true;

        gameManager.close_map();
    }

    private string song_menu_run()
    {
        song_menu_opened = true;

        can_move = false;

        return gameManager.start_songMenu(nearCluster);
    }

    private void song_menu_esc()
    {
        song_menu_opened = false;

        can_move = true;

        gameManager.stop_songMenu();
    }

    public void set_nearCluster(GameObject cluster, bool near_bool)
    {
        nearCluster = cluster;
        is_near = near_bool;
    }

    public void enterCluster(string cluster_id, bool is_leaf, bool starting = false, bool start_call = false)
    {
        if (start_call && !starting) // If we are calling this to start but we already started, we do not do this.
            return;

        if (!starting) {
            current_cluster_id = current_cluster_id + cluster_id;   // Aggiorno il current_cluster_id, che è tenuto all'interno del player.
        }
        PlayerPrefs.SetString("current_cluster_id", current_cluster_id);

        if (!is_leaf)
        {
            gameManager.runClustersInterface(current_cluster_id);
            int delay_seconds = 0;
            Invoke("load_scene", delay_seconds);
        }
        else
        {
            Debug.Log("Il cluster è un cluster foglia!");
        }
        
    }

    public void setSelectedCluster(Transform selected)
    {
        selected_clust_transform = selected;
    }

    public Vector3 get_start()
    {
        Dictionary<string, string> a = gameManager.axis;
        Dictionary<string, float> centroid = gameManager.starting_centroid;
        return new Vector3(centroid[a["axis1"]] * axis_multiplier + 2, centroid[a["axis2"]] * axis_multiplier,centroid[a["axis3"]] * axis_multiplier);
    }


    private void OnApplicationQuit()
    {
        PlayerPrefs.DeleteAll();
    }

    private void load_scene()
    {
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex); // Ricarico la scena
    }

}
