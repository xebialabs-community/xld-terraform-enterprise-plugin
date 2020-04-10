/**
 * Copyright 2020 XEBIALABS
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
 */
package com.xebialabs.deployit.plugin.api.udm.artifact;

import com.xebialabs.deployit.plugin.api.udm.Metadata;
import com.xebialabs.overthere.OverthereFile;

import java.util.ArrayList;
import java.util.List;

import static com.xebialabs.deployit.plugin.api.udm.Metadata.ConfigurationItemRoot.NESTED;

@Metadata(virtual = true, inspectable = false, root = NESTED)
public class LocalEmbeddedDeployableFolder extends EmbeddedDeployableArtifact implements FolderArtifact {

    public List<OverthereFile> getFiles() {
        List<OverthereFile> files = new ArrayList<>();
        OverthereFile folderLocation = getFile();
        if (folderLocation.exists() && folderLocation.isDirectory() && folderLocation.canRead()) {
            List<? extends OverthereFile> allFiles = folderLocation.listFiles();
            if (allFiles != null) {
                files.addAll(allFiles);
            }
        }
        return files;
    }


}
