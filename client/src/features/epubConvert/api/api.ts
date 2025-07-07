import axiosInstance from "../../../lib/axios";

export const convertEpubToMp3 = async (file: File): Promise<Blob> => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axiosInstance.post("/convert", formData, {
    responseType: "blob",
  });

  return res.data;
};
