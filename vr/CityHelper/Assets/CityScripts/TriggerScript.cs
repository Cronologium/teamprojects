using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TriggerScript : MonoBehaviour {

    private GameObject caughtCar;
    public bool stopCars;

	// Use this for initialization
	void Start () {
        caughtCar = null;
        stopCars = true;
	}
	
	// Update is called once per frame
	void Update () {
		if (!stopCars && caughtCar != null)
        {
            caughtCar.GetComponent<CarScript>().launchCar(true);
            caughtCar = null;
        }
	}

    private void OnTriggerEnter(Collider other)
    {
        if (stopCars && caughtCar == null)
        {
            caughtCar = other.gameObject;
            caughtCar.GetComponent<CarScript>().stopCar(true);
        }
    }
}
