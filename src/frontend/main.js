console.log(window.config); 

AWS.config.update({
    region: 'us-east-1',
    credentials: new AWS.Credentials({
        accessKeyId: window.config.ACCESS_KEY, 
        secretAccessKey: window.config.SECRET_KEY 
    })
});


async function uploadToS3Bucket(stream, credential, cd) {
    let s3 = new AWS.S3();
    console.log(s3)
    console.log("depois de abrir sessao AWS", credential.Bucket);
    
    var params = {
        Bucket: credential.Bucket, 
        Key: "largeobject3"
       };
    
       let createMulti;
       try {
           createMulti = await s3.createMultipartUpload(params).promise();
           console.log("Upload multipart criado:", createMulti);
       } catch (err) {
           console.error("Erro ao criar upload multipart:", err);
           return;
       }
       
    const uploadId = createMulti.UploadId;
    const partSize = 5 * 1024 * 1024; // Tamanho de cada parte: 5MB
    const fileSize = stream.byteLength;
    let parts = [];

            // Passo 2: Fazer o upload das partes
    for (let start = 0; start < fileSize; start += partSize) {
        let end = Math.min(start + partSize, fileSize);
        let partNumber = parts.length + 1;
        let partParams = {
                Body: stream.slice(start, end),
                Bucket: credential.Bucket,
                Key: "largeobject3",
                PartNumber: partNumber,
                UploadId: uploadId
            };

        try {
            let part = await s3.uploadPart(partParams).promise();
            parts.push({ ETag: part.ETag, PartNumber: partNumber });
            console.log(`Parte ${partNumber} enviada com sucesso:`, part);
        } catch (err) {
            console.error(`Erro ao enviar a parte ${partNumber}:`, err);
            return;
            }
        }

        console.log("Partes capturadas para o upload multipart:", parts);


        let completeParams = {
                Bucket: credential.Bucket,
                Key: "largeobject3",
                MultipartUpload: {
                    Parts: parts
                },
                UploadId: uploadId
        };

        try {
            let complete = await s3.completeMultipartUpload(completeParams).promise();
            console.log("Upload multipart finalizado com sucesso:", complete);
        } catch (err) {
            console.error("Erro ao finalizar o upload multipart:", err);
        }
}


async function uploadMedia() {
    let credentialRequest = {
        Bucket: 'pooling-application-bucket'
    };
    let mediaStreamRequest = getFile(document.getElementById("fileToUpload").files[0])
    const [mediaStream] = await Promise.all([
        mediaStreamRequest
    ])
    await uploadToS3Bucket(mediaStream, credentialRequest, (progress) => {
        console.log(progress)
    })
}

async function getFile(file) {
    return new Promise((resolve, reject) => {
        let reader = new FileReader();
        reader.onload = (e) => {
            resolve(e.target.result);
        };
        reader.onerror = (err) => {
            reject(false);
        };
        reader.readAsArrayBuffer(file);
    });
};


