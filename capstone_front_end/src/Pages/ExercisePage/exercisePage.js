import React from "react";

import "./exercisePage.css";
import MainSection from "../../Components/MainSection/mainSection";
import MainSide from "../../Components/MainSide/mainSide";
import SecondMain from "../../Components/SecondMain/secondMain";
import SecondSide from "../../Components/SecondSide/secondSide";
import ThirdCenter from "../../Components/ThirdCenter/thirdCenter";
import Button from "../../UIElements/Button/button";

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
          <a href="/mediaPipeOutput">
            <Button title="Try it out" />
          </a>
        </div>
        <div className="oneExercise">
          <div className="exerciseName">Lunges</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/lunges.png")}
          />
          <a href="/mediaPipeOutput">
            <Button title="Try it out" />
          </a>
        </div>
        <div className="oneExercise">
          <div className="exerciseName">Push Up</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/push-up.png")}
          />
          <a href="/mediaPipeOutput">
            <Button title="Try it out" />
          </a>
        </div>
        <div className="oneExercise">
          <div className="exerciseName">Leg Extensions</div>
          <img
            className="exerciseLogo"
            src={require("../../Images/legMachine.png")}
          />
          <a href="/mediaPipeOutput">
            <Button title="Try it out" />
          </a>
          {/* <Button onClickHandler={ / function here / } title="Try it out" /> */}
        </div>
      </div>
    </React.Fragment>
  );
};

export default ExercisePage;
