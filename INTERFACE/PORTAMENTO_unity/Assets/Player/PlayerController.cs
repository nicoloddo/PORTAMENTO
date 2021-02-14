using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class PlayerController : MonoBehaviour
{
    // ASSEGNAZIONI UTILI
    private Animator animator;
    private CharacterController characterController;

    // LINKS
    public GameObject camera;
    public GameManager gameManager;
    private GameObject nearCluster;

    // BOOLS
    public bool is_near = false;
    public bool can_move = true;
    private bool song_menu_opened = false;

    // INPUTS
    private float inputUpward; // Per muoversi verso sù
    private float inputVertical; //Tasti per muoversi in avanti
    private float inputHorizontal; //Tasti per ruotare (oltre al mouse)
    private float totalXRot; //Rotazione in X totale
    private float totalYRot; //Rotazione in Y totale

    // PARAMETRI
    private float rotateSpeedX = 4f; //Velocita' di rotazione X
    private float rotateSpeedY = 3f; //Velocita' di rotazione Y
    public float forwardSpeed = 0.5f; // Velocità di avanzamento
    public float lateralSpeed = 0.2f; // Velocità movimento laterale
    public float upwardSpeed = 0.3f; // Velocità di levitazione

    // NAVIGAZIONE
    public string current_cluster_id = "0";

    private void Awake()
    {
        if (PlayerPrefs.HasKey("current_cluster_id"))
        {
            current_cluster_id = PlayerPrefs.GetString("current_cluster_id");
        }
        else
        {
            current_cluster_id = "0";
        }

        gameManager = FindObjectOfType<GameManager>();
        animator = GetComponent<Animator>();
        characterController = GetComponent<CharacterController>();
    }

    void Start()
    {
        // DEVO RICORDARMI, PRIMA DI AVVIARE IL "VIAGGIO" DI UTILIZZARE LO SCRIPT start_trip.py
        gameManager.runClustersInterface(current_cluster_id);   // All'inizio del caricamento della scena eseguiamo il ClustersInterface
    }

    // Update is called once per frame
    void Update()
    {
        if (Input.GetKey("f") && is_near)
        {
            if(song_menu_opened)
            {
                song_menu_run();
            }
            else
            {
                song_menu_esc();
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

    private void song_menu_run()
    {
        song_menu_opened = true;

        // PREPROCESSING
        can_move = false;

        // ESECUZIONE
        gameManager.start_songMenu(nearCluster);
    }

    private void song_menu_esc()
    {
        song_menu_opened = false;

        gameManager.stop_songMenu();

        //POSTPROCESSING
        can_move = true;
    }

    public void set_nearCluster(GameObject cluster, bool near_bool)
    {
        nearCluster = cluster;
        is_near = near_bool;
    }

    public void enterCluster(string cluster_id)
    {
        current_cluster_id = current_cluster_id + cluster_id;   // Aggiorno il current_cluster_id, che è tenuto all'interno del player.
        PlayerPrefs.SetString("current_cluster_id", current_cluster_id);
        
        SceneManager.LoadScene(SceneManager.GetActiveScene().buildIndex); // Ricarico la scena
    }


    private void OnApplicationQuit()
    {
        PlayerPrefs.DeleteAll();
    }

}
