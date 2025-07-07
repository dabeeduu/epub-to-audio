import DragDropArea from "./components/DragDropArea";
import { useEpubConvert } from "./api/hooks";

const EpubConvertPage = () => {
  const { file, isLoading, handleFileChange, submit } = useEpubConvert();

  return (
    <div className="max-w-xl mx-auto p-5">
      <h1 className="text-2xl font-bold mb-6 text-center">
        EPUB to MP3 Converter
      </h1>

      <DragDropArea onFileSelected={handleFileChange} file={file} />

      <button
        onClick={submit}
        disabled={!file || isLoading}
        className={`w-full mt-5 py-2 px-4 text-lg rounded 
          ${!file || isLoading ? "bg-gray-400 cursor-not-allowed" : "bg-blue-600 hover:bg-blue-700 cursor-pointer"} 
          text-white transition-colors`}
      >
        {isLoading ? "Converting..." : "Submit"}
      </button>
    </div>
  );
};

export default EpubConvertPage;
