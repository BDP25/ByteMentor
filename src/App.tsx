import { useState } from "react";
import Alert from "./components/Alert";
import Button from "./components/Button";

function App() {
  const [alertVisible, setAlertVisiblility] = useState(false)

  return (
    <div>
      { alertVisible && <Alert onClose={() => setAlertVisiblility(false)}>My Alert</Alert>}
      <Button onClick={() => setAlertVisiblility(true)}>
        My Button
      </Button>
    </div>
  );
}

export default App;
