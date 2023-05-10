import React from "react";

import "./exercisePage.css";
import MainSection from "../../Components/MainSection/mainSection";
import MainSide from "../../Components/MainSide/mainSide";
import SecondMain from "../../Components/SecondMain/secondMain";
import SecondSide from "../../Components/SecondSide/secondSide";
import ThirdCenter from "../../Components/ThirdCenter/thirdCenter";
import Button from "../../UIElements/Button/button";
import { useEffect, useState } from "react";

const bicepCulrs = async () => {
  try{
    fetch("http://localhost:5000/bicepcurl", {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  catch(err)
  {
    console.log("Camera feed is exited");
  }
};

const lunges = async () => {
  try{
    fetch("http://localhost:5000/lunges", {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  catch(err)
  {
    console.log("Camera feed is exited");
  }
};

const pushUp = async () => {
  try{
    fetch("http://localhost:5000/pushup", {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  catch(err)
  {
    console.log("Camera feed is exited");
  }
};

const legExtensions = async () => {
  try{
    fetch("http://localhost:5000/legextensions", {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  catch(err)
  {
    console.log("Camera feed is exited");
  }
};


const ExercisePage = () => {
  return (
    <React.Fragment>
      <div className="exerciseHeader">Exercises</div>
      <div className="allExercise">
        <div className="oneExercise">
          <div className="exerciseName">Bicep Curls</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/bicep.png")}
          />
          <Button title="Try it out" onClickHandler={bicepCulrs} />
        </div>
        <div className="oneExercise">
          <div className="exerciseName">Lunges</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/lunges.png")}
          />
          <Button title="Try it out" onClickHandler={lunges} />
        </div>
        <div className="oneExercise">
          <div className="exerciseName">Push Up</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/push-up.png")}
          />
          <Button title="Try it out" onClickHandler={pushUp} />
        </div>
        <div className="oneExercise">
          <div className="exerciseName">Leg Extensions</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/legMachine.png")}
          />
          <Button title="Try it out" onClickHandler={legExtensions} />
        </div>
      </div>
    </React.Fragment>
  );
};

export default ExercisePage;
