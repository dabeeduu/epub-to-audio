import { useState } from "react";
import { convertEpubToMp3 } from "./api";

export const useEpubConvert = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleFileChange = (newFile: File) => {
    setFile(newFile);
  };

  const submit = async () => {
    if (!file) return;

    setIsLoading(true);
    try {
      const zipBlob = await convertEpubToMp3(file);

      const url = URL.createObjectURL(zipBlob);
      const link = document.createElement("a");
      link.href = url;
      link.setAttribute("download", "output.zip");
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    } catch (error) {
      alert("Conversion failed");
    } finally {
      setIsLoading(false);
    }
  };

  return {
    file,
    isLoading,
    handleFileChange,
    submit,
  };
};
