import FileUpload from "../components/FileUpload";
import QueryForm from "../components/QueryForm";
import StatusDisplay from "../components/StatusDisplay";
import ClearData from "../components/ClearData";
import TrainSystem from "../components/TrainSystem";
import { useState } from "react";

function MainPage() {
  const [refreshStatus, setRefreshStatus] = useState(false);

  const handleActionSuccess = () => {
    setRefreshStatus(!refreshStatus); // Trigger status refresh
  };

  return (
    <div className="min-h-screen bg-neutral py-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FileUpload onUploadSuccess={handleActionSuccess} />
          <TrainSystem />
          <QueryForm />
          <StatusDisplay key={refreshStatus} />
          <ClearData onClearSuccess={handleActionSuccess} />
        </div>
      </div>
    </div>
  );
}

export default MainPage;
